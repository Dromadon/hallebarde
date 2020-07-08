resource "aws_s3_bucket_object" "test" {
  for_each = fileset(var.path_to_website_build, "**")

  bucket = aws_s3_bucket.website.id
  key    = each.value
  source = "${var.path_to_website_build}/${each.value}"

  etag = filemd5("${var.path_to_website_build}/${each.value}")
}