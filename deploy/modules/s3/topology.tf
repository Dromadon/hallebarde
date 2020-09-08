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

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
