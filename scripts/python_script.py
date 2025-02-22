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
    s3 = boto3.client('s3')
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
    file_name = "test_file.txt"
    write_weather_to_file(file_name, api_key)
    upload_file(bucket, file_name)