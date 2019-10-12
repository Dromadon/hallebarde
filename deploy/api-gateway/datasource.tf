data "aws_lambda_function" "lambda" {
  function_name = "hallebarde-${var.env}-get-s3-presigned-url"
}

data "aws_caller_identity" "current" {}
