import json
import boto3

def send_to_sns(payload, status_code):
    sns_client = boto3.client('sns')
    sns_client.publish(
        TopicArn='YourSNSTopicARN',
        Message=json.dumps(payload),
        Subject='Processed Payload',
        MessageAttributes={
            'Status': {
                'DataType': 'Number',
                'StringValue': str(status_code)
            }
        }
    )

def send_to_sqs(service_uuid):
    sqs_client = boto3.client('sqs')
    sqs_client.send_message(
        QueueUrl='YourSQSQueueURL',
        MessageBody=service_uuid
    )

def populate_and_send_to_sns(item, status_code):
    response_payload = {
        "firstName": item.get('firstName', {}).get('S', ''),
        "lastName": item.get('lastName', {}).get('S', ''),
        "detailedAddress": item.get('detailedAddress', {}).get('S', ''),
        "lastPingedLocation": item.get('lastPingedLocation', {}).get('S', '')
    }
    send_to_sns(response_payload, status_code)

def send_email_report(total_processed, total_retries, total_success, total_not_processed):
    ses_client = boto3.client('ses')
    subject = 'Batch Processing Report'
    body = (
        f'Total Processed: {total_processed}\n'
        f'Total Retries: {total_retries}\n'
        f'Total Successful Processing (200): {total_success}\n'
        f'Total Not Processed: {total_not_processed}'
    )

    ses_client.send_email(
        Source='sender@example.com',
        Destination={'ToAddresses': ['recipient@example.com']},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )
