# slack_command_app

Provides a custom template based on the approach illustrated in the AWS blog post 
[Slack Integration Blueprints for AWS Lambda](
https://aws.amazon.com/blogs/aws/new-slack-integration-blueprints-for-aws-lambda/).

Slack App
1. Create a Slack Command (`/lookup`)

AWS Components
1. An API Gateway to provide an endpoint to be invoked from a Slack Command.
2. A Lambda Function to perform authentication, some basic checks and send an intermediate response to Slack
   within 3 seconds (Slack requirement).
3. A Lambda Function to perform actual operation which may take more than 3 seconds to finish.
4. A KMS key for encryption in transit for Slack token.
5. A S3 bucket for storing Lambda logs.
