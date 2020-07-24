# slack-command-app

This repo provides the source code for building a Slack App/Bot with AWS API Gateway and Lambda Functions.
This SlackApp can can handle requests triggered from a 
[Slack Command](https://api.slack.com/interactivity/slash-commands)
which will take longer than [3 seconds](https://api.slack.com/events-api) to process, and posts the details back to
the user.

### Overview

![Architecture](assets/SlackApp-ArchitectureOverview.png)

### Setup on Slack

To create a **Slack Command** in Slack (the default command in this repo is **`/lookup`**)
1. Navigate to https://api.slack.com/apps.
2. Select **Create New App** and select **Slash Commands**.
3. Enter the name **`/lookup`** for the command and click **Add Slash Command Integration**.
4. Enter the provided API endpoint URL in the URL field.
5. Copy the **Verification Token** from **Basic Information**.

### Deployment on AWS

Deploy a CloudFormation stack with 
[cloudformation/slack_command_app_template.yaml](cloudformation/slack_command_app_template.yaml), 
that creates the following AWS Components
1. An API Gateway to provide an endpoint to be invoked from a Slack Command.
2. A Lambda Function [lambda/slack_app_immediate_response.py](lambda/slack_app_immediate_response.py) 
   to perform authentication, some basic checks and send an intermediate response to Slack within 3 seconds
   (Slack requirement).
3. A Lambda Function [lambda/slack_app_worker.py](lambda/slack_app_worker.py)
   to perform actual operation which may take more than 3 seconds to finish.
4. A KMS key for encryption in transit for Slack token.
5. A S3 bucket for storing logs.
