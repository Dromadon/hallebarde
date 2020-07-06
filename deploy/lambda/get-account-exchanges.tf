resource "aws_lambda_function" "get_account_exchanges" {
  filename = var.path_to_package
  function_name = "${var.application_name}-${var.env}-get-account-exchanges"
  role = data.aws_iam_role.role_basic.arn
  handler = "hallebarde/get_account_exchanges.handle"

  source_code_hash = filebase64sha256(var.path_to_package)

  runtime = var.python_runtime

  environment {
    variables = {
      ENVIRONMENT = var.env
      APPLICATION_NAME = var.application_name
    }
  }
}
