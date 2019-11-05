variable "env" {}

data "aws_lambda_function" "s3_presigned_url" {
  function_name = "hallebarde-${var.env}-get-s3-presigned-url"
}

data "aws_lambda_function" "create_exchange" {
  function_name = "hallebarde-${var.env}-create-exchange"
}

data "aws_lambda_function" "revoke_exchange" {
  function_name = "hallebarde-${var.env}-revoke-exchange"
}

data "aws_lambda_function" "authorizer" {
  function_name = "hallebarde-${var.env}-authorizer"
}

data "aws_lambda_function" "get_account_exchanges" {
  function_name = "hallebarde-${var.env}-get-account-exchanges"
}

data "aws_caller_identity" "current" {}
