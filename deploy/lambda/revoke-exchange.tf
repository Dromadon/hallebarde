resource "aws_lambda_function" "create_token" {
  filename = var.path_to_package
  function_name = "hallebarde-${var.env}-revoke-exchange"
  role = data.aws_iam_role.role_s3.arn
  handler = "hallebarde/revoke_exchange.handle"

  source_code_hash = filebase64sha256(var.path_to_package)

  runtime = var.python_runtime

  environment {
    variables = {
      ENVIRONMENT = var.env
    }
  }
}