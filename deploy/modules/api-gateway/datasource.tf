variable "env" {}
variable "route53_zone_name" {}
variable "application_name" {}

provider "aws" {
  # us-east-1 instance for getting certificate
  region = "us-east-1"
  alias  = "cert_provider"
}

data aws_acm_certificate "cert" {
  domain      = "${var.env}.api.${var.route53_zone_name}"
  types       = ["AMAZON_ISSUED"]
  statuses    = ["ISSUED"]
  most_recent = true
  provider    = aws.cert_provider
}

data aws_cognito_user_pools "user_pool" {
  name = "${var.application_name}-${var.env}"
}

data "aws_route53_zone" "zone" {
  name         = var.route53_zone_name
  private_zone = false
}

data "aws_lambda_function" "s3_presigned_upload_url" {
  function_name = "${var.application_name}-${var.env}-get-s3-upload-url"
}

data "aws_lambda_function" "s3_presigned_download_url" {
  function_name = "${var.application_name}-${var.env}-get-s3-download-url"
}

data "aws_lambda_function" "create_exchange" {
  function_name = "${var.application_name}-${var.env}-create-exchange"
}

data "aws_lambda_function" "revoke_exchange" {
  function_name = "${var.application_name}-${var.env}-revoke-exchange"
}

data "aws_lambda_function" "upload_authorizer" {
  function_name = "${var.application_name}-${var.env}-upload-authorizer"
}

data "aws_lambda_function" "download_authorizer" {
  function_name = "${var.application_name}-${var.env}-download-authorizer"
}

data "aws_lambda_function" "get_account_exchanges" {
  function_name = "${var.application_name}-${var.env}-get-account-exchanges"
}

data "aws_caller_identity" "current" {}
