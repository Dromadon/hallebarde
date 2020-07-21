variable env {}
variable application_name {}
variable "route53_zone_name" {}

resource "aws_cognito_user_pool" "users" {
  name = "${var.application_name}-${var.env}"

  admin_create_user_config {
    allow_admin_create_user_only = true
  }

  mfa_configuration = "OFF"

  schema {
    attribute_data_type = "String"
    name                = "email"
    required            = true
    mutable             = true

    string_attribute_constraints {
      min_length = 1
      max_length = 100
    }
  }

  username_attributes = [
  "email"]
}

output "user_pool_id" {
  value = aws_cognito_user_pool.users.id
}
