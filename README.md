# aws-sqs-dlq-redriver ![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiYys5THI3OU1Pc3BIUjc0TWV2aGRFaG1nVCtCZ1ZHYVJpcWtnUVBqSWU0bEFldkVPd2Y5c1pzQUo0NzVEZlpCZWtMOEp1VVByRmZPT2dpWnVYU3RtMkJNPSIsIml2UGFyYW1ldGVyU3BlYyI6IlluaFA0SERpdWdQaFNFOHQiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

This serverless app redrives the messages from an SQS DLQ (Dead Letter Queue) back to its source queue. This is helpful when you fix the bug that was causing the messages ending up in DLQ and you need to put the messages back to process.

## App Architecture

![App Architecture](https://github.com/honglu/aws-sqs-dlq-redriver/raw/master/images/app-architecture.png)

1. The app creates a Lambda function that can redrive the messages from an SQS DLQ to its source queues.
1. The app can redrive given number of messages from any given SQS DLQ to its source queues.

## Installation Instructions

1. [Create an AWS account](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html) if you do not already have one and login
1. Go to the app's page on the [Serverless Application Repository](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:303769779339:applications~aws-sqs-dlq-redriver) and click "Deploy"
1. Provide the required app parameters (see parameter details below) and click "Deploy"

## App Parameters

1. `LogLevel` (optional) - Log level for Lambda function logging, e.g., ERROR, INFO, DEBUG, etc. Default: INFO

## App Outputs

1. `SQSDLQRedriverName` - SQS DLQ Redriver Lambda function name.
1. `SQSDLQRedriverArn` - SQS DLQ Redriver Lambda function ARN.

## Usage
You can use the app to redrive messages from any DLQ. To redrive the messages, you will invoke the SQS DLQ Redriver Lambda with the expected input. See [here](https://docs.aws.amazon.com/lambda/latest/dg/invoking-lambda-functions.html) on how to invoke a Lambda function.

### Input
The SQS DLQ Redriver Lambda accepts the following input:
```json
{
    "DLQName": String,
    "MaxMessageCount": Integer
}
```
* `DLQUrl` (required) - The URL of the DLQ queue.
* `MaxMessageCount` (required) - Maximum number of messages to process

Example:
```json
{
    "DLQName": "my-dlq",
    "MaxMessageCount": 100
}
```

### Output
The SQS DLQ Redriver Lambda returns the following output:
```json
{
    "ProcessedMessageCount": Integer
}
```
* `ProcessedMessageCount` (required) - Number of messages that has been processed

Example:
```json
{
    "ProcessedMessageCount": 100
}
```
## License Summary

This code is made available under the MIT license. See the LICENSE file.