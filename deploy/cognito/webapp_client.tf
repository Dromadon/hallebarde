resource "aws_cognito_user_pool_client" "webapp" {
  name = "client"
  user_pool_id = aws_cognito_user_pool.users.id

  supported_identity_providers = [ aws_cognito_identity_provider.google.provider_name ]

  allowed_oauth_flows = [
    "code"
  ]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes = [
    "hallebarde-${var.env}/api",
    "profile",
    "openid",
    "email"
  ]
  callback_urls = [
    "http://localhost:3000/callback"]
}
