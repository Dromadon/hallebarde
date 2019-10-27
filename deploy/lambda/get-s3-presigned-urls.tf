resource "aws_lambda_function" "test_lambda" {
  filename      = "../../app/package/hallebarde.zip"
  function_name = "hallebarde-${var.env}-get-s3-presigned-url"
  role          = "${data.aws_iam_role.role_s3.arn}"
  handler       = "hallebarde/get_presigned_url.handle"

  source_code_hash = "${filebase64sha256("../../app/package/hallebarde.zip")}"

  runtime = "python3.7"
}
