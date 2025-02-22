FROM python:3.9
WORKDIR /app
COPY scripts/ /app/
RUN pip install boto3 requests
CMD ["python", "python_script.py"]
