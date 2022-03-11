# Dino Function
API gateway functions for the path `api-gateway/dino`

## To Deploy

1. Zip Function

`zip dino-function-deploy-package.zip lambda_function.py`

2. Copy File to S3 Bucket

https://s3.console.aws.amazon.com/s3/buckets/dapper-dines-api-functions?region=us-east-1&tab=objects

3. Update Lambda from S3

https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/dinoLambdaFunction?tab=code

Click "Upload From" > S3 location

s3://dapper-dines-api-functions/dino-function-deploy-package.zip

### Logging

https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logStream:group=%252Faws%252Flambda%252FdinoLambdaFunction



