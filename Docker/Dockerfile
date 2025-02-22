FROM python:3.9
WORKDIR /app
COPY ..scripts/python_script.py /app/
RUN pip install boto3
CMD ["python", "python_script.py"]