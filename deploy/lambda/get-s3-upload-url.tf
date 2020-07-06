resource "aws_lambda_function" "s3_presigned_upload_url_lambda" {
  filename = var.path_to_package
  function_name = "${var.application_name}-${var.env}-get-s3-upload-url"
  role = data.aws_iam_role.role_s3.arn
  handler = "hallebarde/get_presigned_upload_url.handle"

  source_code_hash = filebase64sha256(var.path_to_package)

  runtime = var.python_runtime
  timeout = 10

  environment {
    variables = {
      ENVIRONMENT = var.env
      APPLICATION_NAME = var.application_name
    }
  }
}
