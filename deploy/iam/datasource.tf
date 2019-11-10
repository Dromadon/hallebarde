variable "env" {}
variable "google_oidc_application" {}

data "aws_dynamodb_table" "table" {
  name = "hallebarde-${var.env}-table"
}

data "aws_s3_bucket" "bucket" {
  bucket = "hallebarde-storage-${var.env}"
}
