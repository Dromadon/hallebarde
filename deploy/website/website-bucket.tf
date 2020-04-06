resource "aws_s3_bucket" "logs" {
  bucket = "hallebarde-${var.env}-website-logs"
  acl = "log-delivery-write"
}

resource "aws_s3_bucket" "website" {
  bucket = "hallebarde-${var.env}-website"

  logging {
    target_bucket = aws_s3_bucket.logs.bucket
    target_prefix = "website/"
  }

  force_destroy = true

  website {
    index_document = "index.html"
  }

  policy = <<POLICY
{
  "Version":"2012-10-17",
  "Statement":[
    {
      "Sid":"AddPerm",
      "Effect":"Allow",
      "Principal": {
          "AWS": "${aws_cloudfront_origin_access_identity.website_access_identity.iam_arn}"},
      "Action":["s3:GetObject"],
      "Resource":["arn:aws:s3:::hallebarde-${var.env}-website/*"]
    }
  ]
}
POLICY
}