variable "env" {}

resource "aws_s3_bucket" "bucket" {
  bucket = "hallebarde-storage-${var.env}"
  acl    = "private"

  tags = {
    Name        = "Hallebarde Storage for env ${var.env}"
    Environment = "${var.env}"
  }
}
