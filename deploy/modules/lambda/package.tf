resource "aws_s3_bucket" "code_bucket" {
  bucket = "${var.application_name}-${var.env}-package"
  acl    = "private"
}

resource "aws_s3_bucket_object" "code_package" {
  bucket = aws_s3_bucket.code_bucket.id
  key    = "package.zip"
  source = var.package_path

  etag = filemd5(var.package_path)
}