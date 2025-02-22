provider "aws" {
  region = "ap-south-1"
  access_key = var.aws_access_key_id
  secret_key = var.aws_secret_access_key
}

resource "aws_s3_bucket" "weather" {
  bucket = "weather-app"
}

resource "aws_lambda_function" "weather-app" {
  function_name    = "serverless-weather-app"
  filename        = "../lambda/lambda.zip"
  source_code_hash = filebase64sha256("../lambda/lambda.zip")
  role            = aws_iam_role.lambda_exec.arn
  handler         = "index.handler"
  runtime         = "nodejs14.x"
  environment {
    variables = {
      LOG_LEVEL = "info"
      WEATHER_API_KEY = var.weather_api_key
    }
  }
}