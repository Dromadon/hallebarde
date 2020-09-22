resource "aws_s3_bucket" "logs" {
  bucket = "${var.application_name}-${var.env}-website-logs"
  acl    = "log-delivery-write"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket" "website" {
  bucket = "${var.application_name}-${var.env}-website"

  logging {
    target_bucket = aws_s3_bucket.logs.bucket
    target_prefix = "website/"
  }

  force_destroy = true

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
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
      "Action":["s3:GetObject", "s3:ListBucket"],
      "Resource":["arn:aws:s3:::${var.application_name}-${var.env}-website/*", "arn:aws:s3:::${var.application_name}-${var.env}-website"]
    }
  ]
}
POLICY
}