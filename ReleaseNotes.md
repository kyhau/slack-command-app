0.1.0 - 2020-07-19
==================

Initial version
1. Implemented the Cloudformation template [slack_command_app_template.yaml](
   cloudformation/slack_command_app_template.yaml) for creating 
    1. An API Gateway to provide an endpoint to be invoked from a Slack Command.
    2. A Lambda Function to perform authentication, some basic checks and send an intermediate response to Slack
       within 3 seconds (Slack requirement).
    3. A Lambda Function to perform actual operation which may take more than 3 seconds to finish.
    4. A KMS key for encryption in transit for Slack token.
    5. A S3 bucket for storing Lambda logs.
2. Implemented Lambda function [lambda/slack_app_immediate_response.py](lambda/slack_app_immediate_response.py)
3. Implemented Lambda function [lambda/slack_app_worker.py](lambda/slack_app_worker.py)
