variable "env" {}

resource "aws_lambda_function" "lambda" {
  filename      = "../../app/package/authorizer.zip"
  function_name = "hallebarde-${var.env}-authorizer"
  role          = "${data.aws_iam_role.role.arn}"
  handler       = "authorizer.handle"

  source_code_hash = "${filebase64sha256("../../app/package/authorizer.zip")}"

  runtime = "python3.7"
}
