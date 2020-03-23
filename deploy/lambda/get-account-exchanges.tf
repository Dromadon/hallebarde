resource "aws_lambda_function" "get_account_exchanges" {
  filename = var.path_to_package
  function_name = "hallebarde-${var.env}-get-account-exchanges"
  role = data.aws_iam_role.role_basic.arn
  handler = "hallebarde/get_account_exchanges.handle"

  source_code_hash = filebase64sha256(var.path_to_package)

  runtime = var.python_runtime

  environment {
    variables = {
      ENVIRONMENT = var.env
    }
  }
}
