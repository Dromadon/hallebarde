resource "aws_lambda_function" "upload_authorizer" {
  filename      = "../../app/package/hallebarde.zip"
  function_name = "hallebarde-${var.env}-upload-authorizer"
  role          = data.aws_iam_role.role.arn
  handler       = "hallebarde/upload_authorizer.handle"

  source_code_hash = filebase64sha256("../../app/package/hallebarde.zip")

  runtime = "python3.8"

  environment {
    variables = {
      ENVIRONMENT = var.env
    }
  }
}
