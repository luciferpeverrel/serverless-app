import boto3
import os
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Read AWS credentials from environment variables (injected at runtime)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# S3 details
BUCKET_NAME = "example-bucket"
FILE_TO_UPLOAD = "test_file.txt"  # Ensure this file exists in the container
S3_OBJECT_NAME = "uploaded_file.txt"

def upload_to_s3():
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        logger.error("Missing AWS credentials! Make sure environment variables are set.")
        sys.exit(1)

    try:
        # Initialize S3 client using environment variables
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        
        # Upload file
        s3_client.upload_file(FILE_TO_UPLOAD, BUCKET_NAME, S3_OBJECT_NAME)
        logger.info(f"File '{FILE_TO_UPLOAD}' uploaded successfully to bucket '{BUCKET_NAME}'.")
    
    except Exception as e:
        logger.error(f"Failed to upload file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    upload_to_s3()
