import boto3
import os
import logging
import sys
import json  # Import json module

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Read AWS credentials from environment variables (injected at runtime)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

# AWS Resource Details
BUCKET_NAME = "serverless-app-f6d5d3f5"
FILE_TO_UPLOAD = "test_file.txt"  
S3_OBJECT_NAME = "uploaded_file.txt"
LAMBDA_FUNCTION_NAME = "serverless-app"

def upload_to_s3():
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        logger.error("Missing AWS credentials! Make sure environment variables are set.")
        sys.exit(1)

    try:
        # Initialize S3 client
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        
        # Upload file
        s3_client.upload_file(FILE_TO_UPLOAD, BUCKET_NAME, S3_OBJECT_NAME)
        logger.info(f"File '{FILE_TO_UPLOAD}' uploaded successfully to bucket '{BUCKET_NAME}'.")
        
        # Invoke Lambda function
        invoke_lambda(BUCKET_NAME, S3_OBJECT_NAME)
    
    except Exception as e:
        logger.error(f"Failed to upload file: {e}")
        sys.exit(1)

def invoke_lambda(bucket_name, object_key):
    try:
        lambda_client = boto3.client(
            "lambda",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )

        # Properly formatted JSON payload
        payload = json.dumps({"bucket_name": bucket_name, "object_key": object_key})

        response = lambda_client.invoke(
            FunctionName=LAMBDA_FUNCTION_NAME,
            InvocationType="Event",  # Asynchronous execution
            Payload=payload
        )

        logger.info(f"Lambda function '{LAMBDA_FUNCTION_NAME}' invoked successfully.")
        logger.info(f"Response: {response}")

    except Exception as e:
        logger.error(f"Failed to invoke Lambda function: {e}")
        sys.exit(1)

if __name__ == "__main__":
    upload_to_s3()
