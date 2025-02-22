provider "aws" {
  region = "ap-south-1"
}

resource "aws_s3_bucket" "weather" {
  bucket = "serverless-app"
}

resource "aws_iam_role" "lambda_exec" {
  name = "serverless-app-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "lambda_basic_execution" {
  name       = "lambda-basic-execution"
  roles      = [aws_iam_role.lambda_exec.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "serverless-app" {
  function_name    = "serverless-app"
  filename        = "../lambda/Lambda.zip"
  source_code_hash = filebase64sha256("../lambda/Lambda.zip")
  role            = aws_iam_role.lambda_exec.arn
  handler         = "index.handler"
  runtime         = "nodejs22.x"
  environment {
    variables = {
      LOG_LEVEL = "info"

    }
  }
}
