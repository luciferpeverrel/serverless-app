import boto3
import logging
import sys
import os
import requests

def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        return f"Weather in {city}: {temp}°C\n"
    else:
        return f"Failed to fetch weather for {city}\n"

def write_weather_to_file(file_name, api_key):
    try:
        with open(file_name, "w") as f:
            f.write(get_weather("Bengaluru", api_key))
            f.write(get_weather("New York", api_key))
        logging.info("Weather details written to file successfully.")
    except Exception as e:
        logging.error(f"Failed to write to file: {str(e)}")
        sys.exit(1)

def upload_file(bucket_name, file_name):
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    if not aws_access_key or not aws_secret_key:
        logging.error("AWS credentials not found in environment variables.")
        sys.exit(1)

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

    try:
        s3.upload_file(file_name, bucket_name, file_name)
        logging.info(f"Successfully uploaded {file_name} to {bucket_name}")
    except Exception as e:
        logging.error(f"Upload failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bucket = os.getenv("AWS_S3_BUCKET", "example-bucket")
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        logging.error("Weather API key is missing. Ensure WEATHER_API_KEY is set.")
        sys.exit(1)

    file_name = "test_file.txt"
    write_weather_to_file(file_name, api_key)
    upload_file(bucket, file_name)
