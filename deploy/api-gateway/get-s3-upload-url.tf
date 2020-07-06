resource "aws_api_gateway_resource" "s3_presigned_upload_url" {
  path_part = "s3_presigned_upload_url"
  parent_id = aws_api_gateway_rest_api.api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

resource "aws_api_gateway_method" "get_s3_presigned_upload_url" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.s3_presigned_upload_url.id
  http_method = "GET"
  authorization = "CUSTOM"
  authorizer_id = aws_api_gateway_authorizer.lambda_upload_authorizer.id
}

resource "aws_api_gateway_integration" "s3_presigned_upload_url" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.s3_presigned_upload_url.id
  http_method = aws_api_gateway_method.get_s3_presigned_upload_url.http_method
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = data.aws_lambda_function.s3_presigned_upload_url.invoke_arn
}

resource "aws_lambda_permission" "s3_presigned_upload_lambda_permission" {
  statement_id = "${var.application_name}-${var.env}-allow-get-s3-presigned-upload-url"
  action = "lambda:InvokeFunction"
  function_name = data.aws_lambda_function.s3_presigned_upload_url.function_name
  principal = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_deployment.deployment.execution_arn}/*/s3_presigned_upload_url"
}
