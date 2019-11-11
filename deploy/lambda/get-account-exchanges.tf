resource "aws_lambda_function" "get_account_exchanges" {
  filename      = "../../app/package/hallebarde.zip"
  function_name = "hallebarde-${var.env}-get-account-exchanges"
  role          = data.aws_iam_role.role_basic.arn
  handler       = "hallebarde/get_account_exchanges.handle"

  source_code_hash = filebase64sha256("../../app/package/hallebarde.zip")

  runtime = "python3.7"

  environment {
    variables = {
      ENVIRONMENT = var.env
    }
  }
}
