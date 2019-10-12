variable "env" {}

data "aws_lambda_function" "s3_presigned_url" {
  function_name = "hallebarde-${var.env}-get-s3-presigned-url"
}

data "aws_lambda_function" "get_token" {
  function_name = "hallebarde-${var.env}-get-token"
}

data "aws_lambda_function" "authorizer" {
  function_name = "hallebarde-${var.env}-authorizer"
}

data "aws_caller_identity" "current" {}
