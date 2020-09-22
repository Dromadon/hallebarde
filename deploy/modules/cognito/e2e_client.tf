resource "aws_cognito_user_pool_client" "e2e" {
  name         = "${var.application_name}-${var.env}-end2end"
  user_pool_id = aws_cognito_user_pool.users.id

  allowed_oauth_flows = [
  "client_credentials"]
  allowed_oauth_flows_user_pool_client = true
  generate_secret                      = true
  allowed_oauth_scopes                 = aws_cognito_resource_server.resource.scope_identifiers
  callback_urls = [
  "http://localhost:3000/callback"]
}

output "end2end_client_id" {
  value       = aws_cognito_user_pool_client.e2e.id
  description = "The end2end client_id to use for accessing API"
}

output "end2end_client_secret" {
  value       = aws_cognito_user_pool_client.e2e.client_secret
  description = "The end2end client_secret to use for accessing API"
}

output "oauth_domain" {
  value = "${aws_cognito_user_pool_domain.main.domain}.auth.eu-west-1.amazoncognito.com"
}