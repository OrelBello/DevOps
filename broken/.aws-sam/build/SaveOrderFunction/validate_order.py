# src/validate_order.py
import json
import os
import boto3
import logging
import uuid

sqs = boto3.client('sqs')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    try:
        # Extract message from SNS event
        order=event
        # Validate order (similar to previous implementation)
        if not order or 'items' not in order:
            raise ValueError("Invalid order payload")
        
        # Generate unique order ID
        order['order_id'] = str(uuid.uuid4())
        
        # Send validated order to SQS queue
        queue_url = os.environ.get('ORDER_QUEUE_URL')
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(order)
        )
        
        logger.info(f"Order validated: {order['order_id']}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(order)
        }
    
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise