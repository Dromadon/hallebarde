variable "env" {}

data "aws_lambda_function" "s3_presigned_url" {
  function_name = "hallebarde-${var.env}-get-s3-presigned-url"
}

data "aws_lambda_function" "hello_world" {
  function_name = "hallebarde-${var.env}-hello-world"
}

data "aws_lambda_function" "authorizer" {
  function_name = "hallebarde-${var.env}-authorizer"
}

data "aws_caller_identity" "current" {}
