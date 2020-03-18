resource "aws_lambda_function" "download_authorizer" {
  filename      = "../../app/package/hallebarde.zip"
  function_name = "hallebarde-${var.env}-download-authorizer"
  role          = data.aws_iam_role.role.arn
  handler       = "hallebarde/download_authorizer.handle"

  source_code_hash = "${filebase64sha256("../../app/package/hallebarde.zip")}"

  runtime = "python3.7"

  environment {
    variables = {
      ENVIRONMENT = var.env
    }
  }
}