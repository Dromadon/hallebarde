resource "aws_lambda_function" "s3_presigned_upload_url_lambda" {
  function_name = "${var.application_name}-${var.env}-get-s3-upload-url"
  role          = data.aws_iam_role.role_s3.arn
  handler       = "hallebarde/get_presigned_upload_url.handle"

  s3_bucket        = aws_s3_bucket.code_bucket.id
  s3_key           = aws_s3_bucket_object.code_package.id
  source_code_hash = filebase64sha256(var.package_path)

  runtime = var.python_runtime
  timeout = 10

  environment {
    variables = {
      ENVIRONMENT      = var.env
      APPLICATION_NAME = var.application_name
      WEBSITE_HOSTNAME = "${var.env == "prod" ? "" : "${var.env}."}${var.route53_zone_name}"
    }
  }
}
