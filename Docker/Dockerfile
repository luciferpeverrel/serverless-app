FROM python:3.9
WORKDIR /app
COPY scripts/python_script.py /app/
COPY scripts/test_file.txt /app/  
RUN pip install boto3 requests
CMD ["python", "python_script.py"]
