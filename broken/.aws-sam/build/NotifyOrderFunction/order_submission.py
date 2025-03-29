import json
import os
import boto3
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    # Initialize AWS clients
    sns_client = boto3.client('sns')
    stepfunctions_client = boto3.client('stepfunctions')
    dynamodb = boto3.resource('dynamodb')

    try:
        # Parse incoming request body
        body = json.loads(event['body'])
        
        # Validate basic order structure
        validate_order(body)
        
        # Start Step Functions Execution
        state_machine_arn = os.environ['ORDER_PROCESSING_STATE_MACHINE']
        execution_response = stepfunctions_client.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(body)
        )
        
        # Log the execution details
        logger.info(f"Step Functions Execution Started: {execution_response['executionArn']}")
        
        # Publish to SNS topic
        sns_response = sns_client.publish(
            TopicArn=os.environ['ORDER_NOTIFICATION_TOPIC'],
            Message=json.dumps(body),
            Subject='New Order Submission'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Order submitted successfully',
                'messageId': sns_response['MessageId'],
                'executionArn': execution_response['executionArn']
            })
        }
    
    except Exception as e:
        logger.error(f"Error processing order: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

def validate_order(order):
    """
    Basic order validation
    """
    required_fields = ['orderId', 'customerName', 'items', 'totalAmount']
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in order:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate items
    if not order['items'] or not isinstance(order['items'], list):
        raise ValueError("Items must be a non-empty list")
    
    # Validate total amount
    if not isinstance(order['totalAmount'], (int, float)) or order['totalAmount'] <= 0:
        raise ValueError("Total amount must be a positive number")