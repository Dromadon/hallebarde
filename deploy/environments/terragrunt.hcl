generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "eu-west-1"
  version="2.66"
}
EOF
}

remote_state {
  backend = "s3"

  generate = {
    path      = "backend.tf"
    if_exists = "overwrite"
  }

  config = {
    bucket         = "hallebarde-backend"
    key            = "${path_relative_to_include()}"
    region         = "eu-west-1"
    dynamodb_table = "hallebarde-backend-lock"
  }
}

inputs = {
  route53_zone_name                 = "filetransfer.beta.octo.tools"
  application_name                  = "${local.application_name}"
  google_oidc_application_client_id = "274210205449-bend56f57m2gcu9an3q6dmv0atj3i7h1.apps.googleusercontent.com"
  // oidc client secret
}

locals {
  application_name = "filetransfer"
}