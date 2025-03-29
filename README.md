# AWS Serverless Order Processing (Misconfigured)

## Prerequisites
- AWS CLI & AWS SAM CLI installed
- AWS account with deployment permissions

## Deployment Steps
1. Clone repo & navigate to the project:
   ```sh
   git clone git@github.com:OrelBello/DevOps.git && cd broken
   ```
2. Build & deploy:
   ```sh
   sam build && sam deploy --guided
   ```
3. Test the API:
   ```sh
   curl -X POST https://your-api-id.execute-api.region.amazonaws.com/prod/orders \
     -H "Content-Type: application/json" \
     -d '{
         "orderId": "12345678",
         "customerName": "Johnny Lawrance",
         "items": [
             {"product_Id": "PROD0012", "quantity": 21},
             {"product_Id": "PROD0022", "quantity": 12}
         ],
         "totalAmount": 99.99
     }'
   ```

## Assignment Objectives
Investigate and resolve issues affecting the functionality of this serverless architecture. Identify misconfigurations and apply the necessary fixes to restore a fully operational workflow.

### Goal
Debug & fix broken configurations in a serverless environment using AWS tools. 

