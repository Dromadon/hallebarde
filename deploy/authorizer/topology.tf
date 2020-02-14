variable "env" {}

resource "aws_lambda_function" "lambda" {
  filename      = "../../app/package/hallebarde.zip"
  function_name = "hallebarde-${var.env}-authorizer"
  role          = data.aws_iam_role.role.arn
  handler       = "hallebarde/authorizer.handle"

  source_code_hash = "${filebase64sha256("../../app/package/hallebarde.zip")}"

  runtime = "python3.7"

  environment {
    variables = {
      ENVIRONMENT = var.env
    }
  }
}
