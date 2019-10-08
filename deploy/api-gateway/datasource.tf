data "aws_lambda_function" "lambda" {
  function_name = "test-hallebarde"
  qualifier     = "4"
}

data "aws_caller_identity" "current" {}
