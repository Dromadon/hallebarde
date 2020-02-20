resource "aws_cognito_user_pool_domain" "main" {
  domain = "hallebarde-${var.env}"
  user_pool_id = aws_cognito_user_pool.users.id
}

resource "aws_cognito_user_pool_client" "e2e" {
  name = "hallebarde-${var.env}-end2end"
  user_pool_id = aws_cognito_user_pool.users.id

  allowed_oauth_flows = [
    "client_credentials"]
  allowed_oauth_flows_user_pool_client = true
  generate_secret = true
  allowed_oauth_scopes = aws_cognito_resource_server.resource.scope_identifiers
  callback_urls = [
    "http://localhost:3000/callback"]
}

resource "aws_cognito_resource_server" "resource" {
  identifier = "hallebarde-${var.env}"
  name = "hallebarde-${var.env}"

  scope {
    scope_name = "api"
    scope_description = "full api access"
  }

  user_pool_id = aws_cognito_user_pool.users.id
}