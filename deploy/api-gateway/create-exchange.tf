resource "aws_api_gateway_resource" "exchange" {
  path_part   = "exchange"
  parent_id   = "${aws_api_gateway_rest_api.api.root_resource_id}"
  rest_api_id = "${aws_api_gateway_rest_api.api.id}"
}

resource "aws_api_gateway_method" "exchange_get" {
  rest_api_id   = "${aws_api_gateway_rest_api.api.id}"
  resource_id   = "${aws_api_gateway_resource.exchange.id}"
  http_method   = "POST"
  authorization = "AWS_IAM"
}

resource "aws_api_gateway_integration" "token_integration" {
  rest_api_id             = "${aws_api_gateway_rest_api.api.id}"
  resource_id             = "${aws_api_gateway_resource.exchange.id}"
  http_method             = "${aws_api_gateway_method.exchange_get.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${data.aws_lambda_function.create_exchange.invoke_arn}"
}

resource "aws_lambda_permission" "create_exchange_lambda_permission" {
  statement_id  = "hallebarde-${var.env}-allow-create-exchange"
  action        = "lambda:InvokeFunction"
  function_name = "${data.aws_lambda_function.create_exchange.function_name}"
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_deployment.deployment.execution_arn}/*/exchange"
}

