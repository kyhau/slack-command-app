import boto3
import json
import logging
import os
from base64 import b64decode
from urllib.parse import parse_qs

ENCRYPTED = os.environ["KmsEncryptedToken"]
# Decrypt code should run once and variables stored outside of the function
# handler so that these are decrypted once per container
expected_token = boto3.client("kms").decrypt(
    CiphertextBlob=b64decode(ENCRYPTED),
    EncryptionContext={"LambdaFunctionName": os.environ["AWS_LAMBDA_FUNCTION_NAME"]},
)["Plaintext"].decode("utf-8")

logging.getLogger().setLevel(logging.INFO)

child_lambda_name = os.environ["WorkerLambdaFunctionName"]
lambda_client = boto3.client("lambda")


def respond(res, err=None):
    return {
        "body": str(err) if err else json.dumps(res),
        "headers": {
            "Content-Type": "application/json",
        },
        "statusCode": "400" if err else "200",
    }


def invoke_lambda(function_namme, payload_json):
    payload_str = json.dumps(payload_json)
    payload_bytes_arr = bytes(payload_str, encoding="utf8")
    return lambda_client.invoke(
        FunctionName=function_namme,
        InvocationType="Event",  # asynchronous invocation
        Payload=payload_bytes_arr
    )


def lambda_handler(event, context):
    params = parse_qs(event["body"])
    token = params["token"][0]
    if token != expected_token:
        logging.error("Request token (%s) does not match expected ", token)
        return respond(None, err=Exception("Invalid request token"))

    user = params["user_name"][0]
    user_id = params["user_id"][0]
    command = params["command"][0]
    channel = params["channel_name"][0]
    command_text = params.get("text", [None])[0]
    logging.info(f"{user} invoked {command} in {channel} with the following text: {command_text}")

    message = None
    
    if command == "/lookup" and command_text:
        payload = {k: v for k, v in params.items() if k not in ["token", "trigger_id"]}

        resp = invoke_lambda(child_lambda_name, payload)
        if resp["ResponseMetadata"]["HTTPStatusCode"] in [200, 201, 202]:
            message = f"Processing request from <@{user_id}> on {channel}: {command} {command_text}"
        else:
            logging.error(resp)
            message = f"Sorry <@{user_id}>, your request on {channel} ({command} {command_text}) cannot be" \
                      + " processed at the moment. Please try again later."

    if message is None:
        message = f"Sorry @{user_id}>, I do not support {command} {command_text}."

    logging.info(message)
    resp = {
        "response_type": "in_channel",    # visible to all channel members
        "text": message,
    }
    return respond(resp)
