variable "env" {}
variable "route53_zone_name" {}

data "aws_route53_zone" "zone" {
  name = var.route53_zone_name
  private_zone = false
}

provider "aws" {
  # We force region to us-east-1 as certificates must be located there for gateway domain name to use them
  version = "2.53"
  region = "us-east-1"
}