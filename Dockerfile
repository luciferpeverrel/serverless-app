FROM python:3.9
WORKDIR /app
COPY python_script.py /app/
COPY test_file.txt /app/
RUN pip install boto3 requests
CMD ["python", "python_script.py"]
