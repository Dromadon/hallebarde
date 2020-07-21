resource "aws_lambda_function" "s3_presigned_download_url" {
  function_name = "${var.application_name}-${var.env}-get-s3-download-url"
  role          = data.aws_iam_role.role_s3.arn
  handler       = "hallebarde/get_presigned_download_url.handle"

  s3_bucket = aws_s3_bucket.code_bucket.id
  s3_key    = aws_s3_bucket_object.code_package.id

  runtime = var.python_runtime
  timeout = 10

  environment {
    variables = {
      ENVIRONMENT      = var.env
      APPLICATION_NAME = var.application_name
    }
  }
}
