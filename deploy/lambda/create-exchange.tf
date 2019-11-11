resource "aws_lambda_function" "create_exchange" {
  filename      = "../../app/package/hallebarde.zip"
  function_name = "hallebarde-${var.env}-create-exchange"
  role          = data.aws_iam_role.role_basic.arn
  handler       = "hallebarde/create_exchange.handle"

  source_code_hash = filebase64sha256("../../app/package/hallebarde.zip")

  runtime = "python3.7"

  environment {
    variables = {
      ENVIRONMENT = var.env
    }
  }
}
