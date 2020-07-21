variable "env" {}
variable "application_name" {}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "bucket" {
  bucket = "${var.application_name}-${var.env}-storage"
  acl    = "private"

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "POST"]
    allowed_origins = ["*"]
  }

  tags = {
    Name        = "${var.application_name} storage for env ${var.env}"
    Environment = var.env
  }
}
