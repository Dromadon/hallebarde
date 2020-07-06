variable "env" {}
variable "google_oidc_application_client_id" {}
variable "application_name" {}

data "aws_dynamodb_table" "table" {
  name = "${var.application_name}-${var.env}-table"
}

data "aws_s3_bucket" "bucket" {
  bucket = "${var.application_name}-${var.env}-storage"
}
