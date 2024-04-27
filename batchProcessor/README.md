# ACTIVE DIRECTORY SERVICE (An Event-Driven Serverless Architecture with AWS Lambda)

## Overview

This architecture demonstrates an event-driven serverless solution using AWS Lambda, S3, DynamoDB, SNS, and SQS. The system processes batch files uploaded to an S3 bucket, interacts with DynamoDB for data retrieval, and sends notifications via SNS. It also handles retries using SQS.

## Components

- **AWS Lambda**: Processes batch files, interacts with DynamoDB, and sends notifications.
- **Amazon S3**: Batch processing files are uploaded and pulled from the s3 bucket by services.
- **Amazon DynamoDB**: Stores the details of user.
- **Amazon SNS**: Notification service to notify multiple microservices.
- **Amazon SQS**: A simple FIFO queue to queue the records meant for retrying temporarily.

## File Structure

.
├── lambda_function.py # Main Lambda function code
├── helper ├──helper_functions.py # Helper functions used by Lambda
├── resources.yaml # cloudformation yaml template to create all the resources in one step
└── README.md # Documentation


## Prerequisites

- AWS Free Tier Account
- Python 3.x
- AWS CLI configured with appropriate permissions

## Setup

1. **Resources Setup in AWS:**
   - Let us first set up the AWS services required to run this application:
      * Log in to your AWS account and navigate to the AWS Management Console.
      * In the AWS Management Console, search for "CloudFormation" and open it in a new tab.
      * In the CloudFormation dashboard, click on "Stacks" on the left-hand side to view your current CloudFormation stacks.
      * Click on "Create stack" and select "With new resources".
      * Choose "Upload a template file" and upload the `resources.yaml` file provided with the project.
      * Click "Next" and provide a name for your CloudFormation stack (e.g., ADSresources) in Step 2.
      * Select "Dev" as the environment and keep other settings as default. Acknowledge the terms and conditions.
      * Click "Create".
      * Allow some time for the CloudFormation stack to create all the necessary AWS resources.
      * You can monitor the resource creation and any failure logs by navigating to:
         - Stacks -> ADSresources -> Events

2. **List of Resources Created by the CloudFormation Template:**

   - S3 bucket for batch processing
   - Lambda function for event-driven processing
   - SQS queue for message queuing
   - SNS topic for notifications
   
   <!-- Add more details based on the resources created -->
   
3. **Manually Uploading Code to Lambda Function:**

   After the CloudFormation stack is created, you can manually upload the Lambda function code to the Lambda function:

   - Navigate to the AWS Lambda service in the AWS Management Console.
   - Find the Lambda function created by the CloudFormation stack (named something like `LambdaFunction`).
   - Click on the Lambda function to open its details.
   - Scroll down to the "Function code" section.
   - Click on the "Upload from" dropdown and select "`.zip file`".
   - Click on the "Upload" button and select the ZIP file containing your Lambda function code.
   - Once the file is uploaded, click on "Save" to update the Lambda function with the new code.

4. **S3 Event Notification:**

   The CloudFormation template sets up an S3 event notification to trigger the Lambda function whenever a file with the prefix "ADS_Manually_Process_" and suffix of today's date in format DD-MM-YYY is uploaded to the S3 bucket. for eg: 

   - When a file with the specified prefix is uploaded to the S3 bucket, S3 sends a notification to the Lambda function.
   - The Lambda function is then triggered to process the file according to the specified logic.

   This event-driven architecture ensures that the Lambda function is automatically invoked in response to file uploads, enabling seamless batch processing.


## Usage

1. Upload a batch file with the name format `DES_Manually_Process_DD-MM-YYYY` to the configured S3 bucket.
2. Lambda function will process the file:
   - Retry requests with a 5XX status code and retry count <= 1.
   - Retrieve user records from DynamoDB based on `serviceUUID`.
   - Send notifications via SNS.
   - Handle retries using SQS.
3. Processed files will be renamed to `DES_Manually_Processed_<todays-date>` in the S3 bucket.
4. Receive an email report with processing statistics.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
NA
