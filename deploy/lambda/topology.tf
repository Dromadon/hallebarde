variable "env" {}

resource "aws_lambda_function" "test_lambda" {
  filename      = "../../app/get-presigned-url.zip"
  function_name = "hallebarde-${var.env}-get-s3-presigned-url"
  role          = "${data.aws_iam_role.role.arn}"
  handler       = "get-presigned-url.handler"

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  source_code_hash = "${filebase64sha256("../../app/get-presigned-url.zip")}"

  runtime = "python3.7"

  environment {
    variables = {
      foo = "bar"
    }
  }
}
