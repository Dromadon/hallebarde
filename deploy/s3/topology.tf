variable "env" {}

resource "aws_s3_bucket" "bucket" {
  bucket = "hallebarde-storage-${var.env}"
  acl    = "private"

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "POST"]
    allowed_origins = ["*"]
  }

  tags = {
    Name        = "Hallebarde Storage for env ${var.env}"
    Environment = var.env
  }
}
