resource "aws_lambda_function" "get_account_exchanges" {
  function_name = "${var.application_name}-${var.env}-get-account-exchanges"
  role          = data.aws_iam_role.role_basic.arn
  handler       = "hallebarde/get_account_exchanges.handle"

  s3_bucket = aws_s3_bucket.code_bucket.id
  s3_key    = aws_s3_bucket_object.code_package.id

  runtime = var.python_runtime

  environment {
    variables = {
      ENVIRONMENT      = var.env
      APPLICATION_NAME = var.application_name
    }
  }
}
