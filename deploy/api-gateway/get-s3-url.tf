resource "aws_api_gateway_resource" "s3_presigned_url" {
  path_part = "s3_presigned_url"
  parent_id = aws_api_gateway_rest_api.api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

resource "aws_api_gateway_method" "s3_get" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.s3_presigned_url.id
  http_method = "GET"
  authorization = "CUSTOM"
  authorizer_id = aws_api_gateway_authorizer.authorizer.id
}

resource "aws_api_gateway_integration" "s3_integration" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.s3_presigned_url.id
  http_method = aws_api_gateway_method.s3_get.http_method
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = data.aws_lambda_function.s3_upload_url.invoke_arn
}

resource "aws_lambda_permission" "s3_lambda_permission" {
  statement_id = "hallebarde-${var.env}-allow-get-s3-presigned-url"
  action = "lambda:InvokeFunction"
  function_name = data.aws_lambda_function.s3_upload_url.function_name
  principal = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_deployment.deployment.execution_arn}/*/s3_presigned_url"
}

resource "aws_api_gateway_authorizer" "authorizer" {
  name = "hallebarde-${var.env}-token-authorizer"
  rest_api_id = aws_api_gateway_rest_api.api.id
  type = "TOKEN"
  authorizer_result_ttl_in_seconds = 0
  identity_source = "method.request.header.authorizationToken"

  authorizer_uri = data.aws_lambda_function.authorizer.invoke_arn
  authorizer_credentials = aws_iam_role.authorizer_invocation_role.arn
}

resource "aws_iam_role" "authorizer_invocation_role" {
  name = "hallebarde-${var.env}-authorizer-invocation"
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

resource "aws_iam_role_policy" "authorizer_invocation_policy" {
  name = "hallebarde-${var.env}-authorizer-invocation"
  role = aws_iam_role.authorizer_invocation_role.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "lambda:InvokeFunction",
      "Effect": "Allow",
      "Resource": "${data.aws_lambda_function.authorizer.arn}"
    }
  ]
}
EOF
}
