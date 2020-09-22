resource "aws_cognito_user_pool_domain" "main" {
  domain       = "${var.env == "prod" ? "" : "${var.env}-"}${var.application_name}"
  user_pool_id = aws_cognito_user_pool.users.id
}

resource "aws_cognito_resource_server" "resource" {
  identifier = "hallebarde-${var.env}"
  name       = "hallebarde-${var.env}"

  scope {
    scope_name        = "api"
    scope_description = "full api access"
  }

  user_pool_id = aws_cognito_user_pool.users.id
}