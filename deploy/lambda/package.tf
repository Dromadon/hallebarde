resource "aws_s3_bucket" "code_bucket" {
  bucket = "${var.application_name}-${var.env}-package"
  acl    = "private"
}

resource "aws_s3_bucket_object" "code_package" {
  bucket = aws_s3_bucket.code_bucket.id
  key    = "package.zip"
  source = var.path_to_package

  etag = filemd5(var.path_to_package)
}