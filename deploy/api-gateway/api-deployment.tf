resource "aws_api_gateway_rest_api" "api" {
  name = "hallebarde-${var.env}"
  description = "This is my API for demonstration purposes"
}

resource "aws_api_gateway_deployment" "deployment" {
  depends_on = [
    "aws_api_gateway_integration.s3_integration",
    "aws_api_gateway_integration.token_integration",
    "aws_api_gateway_integration.account_exchanges_integration"]

  rest_api_id = "${aws_api_gateway_rest_api.api.id}"
  stage_name = "${var.env}"
  variables = {
    deployed_at = timestamp()
  }
}

