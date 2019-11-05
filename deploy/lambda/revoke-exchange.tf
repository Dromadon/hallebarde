resource "aws_lambda_function" "create_token" {
  filename      = "../../app/package/hallebarde.zip"
  function_name = "hallebarde-${var.env}-revoke-exchange"
  role          = "${data.aws_iam_role.role_basic.arn}"
  handler       = "hallebarde/revoke_exchange.handle"

  source_code_hash = "${filebase64sha256("../../app/package/hallebarde.zip")}"

  runtime = "python3.7"

  environment {
    variables = {
      ENVIRONMENT = var.env
    }
  }
}