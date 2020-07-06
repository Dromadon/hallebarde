resource "aws_api_gateway_resource" "exchanges" {
  path_part = "exchanges"
  parent_id = aws_api_gateway_rest_api.api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

resource "aws_api_gateway_method" "create_exchange" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.exchanges.id
  http_method = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.cognito_authorizer.id
  authorization_scopes = ["hallebarde-${var.env}/api"]
}

resource "aws_api_gateway_integration" "create_exchange" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.exchanges.id
  http_method = aws_api_gateway_method.create_exchange.http_method
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = data.aws_lambda_function.create_exchange.invoke_arn
}

resource "aws_lambda_permission" "create_exchange_lambda_permission" {
  statement_id = "${var.application_name}-${var.env}-allow-create-exchange"
  action = "lambda:InvokeFunction"
  function_name = data.aws_lambda_function.create_exchange.function_name
  principal = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_deployment.deployment.execution_arn}/*/exchanges"
}

