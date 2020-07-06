resource "aws_lambda_function" "revoke_exchange" {
  filename = var.path_to_package
  function_name = "${var.application_name}-${var.env}-revoke-exchange"
  role = data.aws_iam_role.role_s3.arn
  handler = "hallebarde/revoke_exchange.handle"

  source_code_hash = filebase64sha256(var.path_to_package)

  runtime = var.python_runtime

  environment {
    variables = {
      ENVIRONMENT = var.env
      APPLICATION_NAME = var.application_name
    }
  }
}
