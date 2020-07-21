variable "google_oidc_application_client_id" {}
variable "google_oidc_application_client_secret" {}

resource "aws_cognito_identity_provider" "google" {
  user_pool_id  = aws_cognito_user_pool.users.id
  provider_name = "Google"
  provider_type = "Google"

  provider_details = {
    authorize_scopes = "email openid"
    client_id        = var.google_oidc_application_client_id
    client_secret    = var.google_oidc_application_client_secret
  }

  attribute_mapping = {
    email    = "email"
    username = "sub"
  }
}