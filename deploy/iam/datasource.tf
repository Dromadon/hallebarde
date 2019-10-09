data "aws_s3_bucket" "bucket" {
  bucket = "hallebarde-storage-${var.env}"
}
