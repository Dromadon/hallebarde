resource "aws_lambda_function" "create_exchange" {
  filename = var.path_to_package
  function_name = "hallebarde-${var.env}-create-exchange"
  role = data.aws_iam_role.role_basic.arn
  handler = "hallebarde/create_exchange.handle"

  source_code_hash = filebase64sha256(var.path_to_package)

  runtime = var.python_runtime

  environment {
    variables = {
      ENVIRONMENT = var.env
    }
  }
}
