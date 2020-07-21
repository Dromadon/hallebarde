resource "aws_cognito_user_pool_client" "webapp" {
  name         = "web_client"
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
  callback_urls = ["https://${var.env == "prod" ? "" : "${var.env}."}${var.route53_zone_name}/callback"]
  logout_urls = ["https://${var.env == "prod" ? "" : "${var.env}."}${var.route53_zone_name}/signout"]
}

output "web_client_id" {
  value = aws_cognito_user_pool_client.webapp.id
}

output "web_client_callback_url" {
  value = sort(aws_cognito_user_pool_client.webapp.callback_urls)[0]
}

output "web_client_signout_url" {
  value = sort(aws_cognito_user_pool_client.webapp.logout_urls)[0]
}