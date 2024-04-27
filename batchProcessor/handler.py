import json
import boto3
import datetime
from helper.helper_functions import send_to_sns, send_to_sqs, populate_and_send_to_sns, send_email_report

s3_client = boto3.client('s3')
dynamodb_client = boto3.client('dynamodb')
sns_client = boto3.client('sns')
sqs_client = boto3.client('sqs')
ses_client = boto3.client('ses')

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    file_content = response['Body'].read().decode('utf-8')
    
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')
    processed_file_key = f"DES_Manually_Processed_{today_date}"
    
    total_processed = 0
    total_retries = 0
    total_success = 0
    total_not_processed = 0
    
    for line in file_content.split('\n'):
        if not line.strip():
            continue
        status_code, retry_count, service_uuid = line.strip().split(',')
        
        status_code = int(status_code)
        retry_count = int(retry_count)

        if status_code >= 500 and status_code < 600 and retry_count <= 1:
            total_retries += 1
            send_to_sqs(service_uuid)
        
        else:
            response = dynamodb_client.get_item(
                TableName='YourDynamoDBTableName',
                Key={'serviceUUID': {'S': service_uuid}}
            )

            item = response.get('Item')
            
            if item:
                status = item.get('status', {}).get('S')
                
                if status == 'Active':
                    total_success += 1
                    populate_and_send_to_sns(item, 200)
                
                else:
                    total_not_processed += 1
                    populate_and_send_to_sns({"message": "Cannot process the request as the user is either not a member or hasn't been onboarded yet."}, 200)
            
            else:
                total_not_processed += 1
                populate_and_send_to_sns({"message": "Cannot process the request as the user is either not a member or hasn't been onboarded yet."}, 200)
        
        total_processed += 1

    # Rename the processed file
    s3_client.copy_object(
        Bucket=bucket_name,
        CopySource={'Bucket': bucket_name, 'Key': file_key},
        Key=processed_file_key
    )
    s3_client.delete_object(Bucket=bucket_name, Key=file_key)

    send_email_report(total_processed, total_retries, total_success, total_not_processed)
