resource "aws_lambda_function" "hello_world" {
  filename      = "../../app/package/hello-world.zip"
  function_name = "hallebarde-${var.env}-hello-world"
  role          = "${data.aws_iam_role.role_basic.arn}"
  handler       = "hello-world.handle"

  source_code_hash = "${filebase64sha256("../../app/package/hello-world.zip")}"

  runtime = "python3.7"
}
