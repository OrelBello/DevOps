# src/save_order.py
import json
import boto3
import uuid
import os

dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    try:
        # Potential issue: No table name environment variable
        table_name = os.environ.get('ORDERS_TABLE', 'Orders')
        table = dynamodb.Table(table_name)
        
        # Parsing order (might fail due to previous lambda's output)
        order = json.loads(event['body'])
        
        # Generate order ID - potential race condition
        order_id = str(uuid.uuid4())
        order['OrderId'] = order_id
        
        # Intentional lack of comprehensive error handling
        response = table.put_item(Item=order)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Order saved successfully',
                'orderId': order_id
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }