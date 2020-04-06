variable "route53_zone_name" {}

data "aws_route53_zone" "zone" {
  name = var.route53_zone_name
  private_zone = false
}

provider "aws" {
  # us-east-1 instance for getting certificate
  region = "us-east-1"
  alias = "cert_provider"
}

data aws_acm_certificate "cert" {
  domain      = "${var.env}.${var.route53_zone_name}"
  types       = ["AMAZON_ISSUED"]
  statuses = ["ISSUED"]
  most_recent = true
  provider = aws.cert_provider
}