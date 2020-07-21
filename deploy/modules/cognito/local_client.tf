resource "aws_cognito_user_pool_client" "local" {
  name         = "local"
  user_pool_id = aws_cognito_user_pool.users.id

  supported_identity_providers = [aws_cognito_identity_provider.google.provider_name]

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
  callback_urls = ["http://localhost:3000/callback"]
  logout_urls = ["http://localhost:3000/signout"]
  count         = var.env == "prod" ? 0 : 1
}

output "local_client_id" {
  value = length(aws_cognito_user_pool_client.local) > 0 ? aws_cognito_user_pool_client.local[0].id : null
}

output "local_client_callback_url" {
  value = length(aws_cognito_user_pool_client.local) > 0 ? sort(aws_cognito_user_pool_client.local[0].callback_urls)[0] : null
}

output "local_client_signout_url" {
  value = length(aws_cognito_user_pool_client.local) > 0 ? sort(aws_cognito_user_pool_client.local[0].logout_urls)[0] : null
}