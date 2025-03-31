# src/notify_order.py
import json
import os
import boto3
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)
time.sleep(5)
def handler(event, context):
    try:
        # Extract message from SNS event
        order = json.loads(event['body'])
        
        # Log notification details
        logger.info(f"Processing notification for order: {order.get('order_id')}")
        
        # Here you could implement additional notification logic
        # Such as sending emails, SMS, etc.
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Notification processed'})
        }
    
    except Exception as e:
        logger.error(f"Notification error: {str(e)}")
        raise
