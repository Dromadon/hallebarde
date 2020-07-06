resource "aws_api_gateway_authorizer" "lambda_upload_authorizer" {
  name = "${var.application_name}-${var.env}-upload-token-authorizer"
  rest_api_id = aws_api_gateway_rest_api.api.id
  type = "TOKEN"
  authorizer_result_ttl_in_seconds = 0
  identity_source = "method.request.header.Authorization"
  authorizer_uri = data.aws_lambda_function.upload_authorizer.invoke_arn
  authorizer_credentials = aws_iam_role.upload_authorizer_invocation_role.arn
}

resource "aws_iam_role" "upload_authorizer_invocation_role" {
  name = "${var.application_name}-${var.env}-upload-authorizer-invocation"
  path = "/"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "apigateway.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "upload_authorizer_invocation_policy" {
  name = "${var.application_name}-${var.env}-upload-authorizer-invocation"
  role = aws_iam_role.upload_authorizer_invocation_role.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "lambda:InvokeFunction",
      "Effect": "Allow",
      "Resource": "${data.aws_lambda_function.upload_authorizer.arn}"
    }
  ]
}
EOF
}
