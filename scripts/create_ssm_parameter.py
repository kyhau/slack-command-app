from boto3.session import Session
import logging

logging.getLogger().setLevel(logging.INFO)

key_id = "TODO The KMS Key ID"
parameter_key = "/apps/slack_app/xxx/token"
slack_app_name = "slack-command"
token = "TODO The Slack App Token"

session = Session(profile_name="default")

resp = session.client("ssm").put_parameter(
    Name=parameter_key,
    Description=f"Slack App {slack_app_name} Token",
    Value=token,
    Type="SecureString",
    KeyId=key_id,
    Tags=[
        {
            "Key": "Billing",
            "Value": "Slack App",
        }
    ],
)

print(resp)
