resource "aws_lambda_function" "get_token" {
  filename      = "../../app/package/get_token.zip"
  function_name = "hallebarde-${var.env}-get-token"
  role          = "${data.aws_iam_role.role_basic.arn}"
  handler       = "get_token.handle"

  source_code_hash = "${filebase64sha256("../../app/package/get_token.zip")}"

  runtime = "python3.7"
}
