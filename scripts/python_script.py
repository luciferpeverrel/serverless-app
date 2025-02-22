import boto3
import logging
import sys

def upload_file(bucket_name, file_name):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(f"../scripts/{file_name}", bucket_name, file_name)
        logging.info(f"Successfully uploaded {file_name} to {bucket_name}")
    except Exception as e:
        logging.error(f"Upload failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    upload_file("serverless-weather-app", "test_file.txt")