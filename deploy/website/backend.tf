terraform {
  backend "s3" {}
}

provider "aws" {
  region = "eu-west-1"
  version = "2.54"
}
