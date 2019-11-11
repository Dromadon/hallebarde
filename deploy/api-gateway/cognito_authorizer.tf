resource "aws_api_gateway_authorizer" "cognito_authorizer" {
  name = "hallebarde-${var.env}-cognito-authorizer"
  type = "COGNITO_USER_POOLS"
  identity_source = "method.request.header.Authorization"
  rest_api_id = aws_api_gateway_rest_api.api.id
  provider_arns = data.aws_cognito_user_pools.user_pool.arns
}
