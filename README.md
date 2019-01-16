# aws-sqs-dlq-redriver ![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiYys5THI3OU1Pc3BIUjc0TWV2aGRFaG1nVCtCZ1ZHYVJpcWtnUVBqSWU0bEFldkVPd2Y5c1pzQUo0NzVEZlpCZWtMOEp1VVByRmZPT2dpWnVYU3RtMkJNPSIsIml2UGFyYW1ldGVyU3BlYyI6IlluaFA0SERpdWdQaFNFOHQiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

This serverless app redrives the messages from an SQS DLQ (Dead Letter Queue) back to its source queue. This is helpful when you fix the bug that was causing the messages ending up in DLQ and you need to put the messages back to process.

## App Architecture

TODO: arch diagram

## Installation Instructions

1. [Create an AWS account](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html) if you do not already have one and login
1. Go to the app's page on the [Serverless Application Repository](TODO) and click "Deploy"
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

### Output
The SQS DLQ Redriver Lambda returns the following output:

## License Summary

This code is made available under the MIT license. See the LICENSE file.