variable "env" {}

resource "aws_iam_policy" "policy" {
  name        = "hallebarde-${var.env}-s3-presigned-url"
  path        = "/hallebarde/"
  description = "Allows hallebarde to create s3 presigned urls in hallebarde bucket"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
{
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "${data.aws_s3_bucket.bucket.arn}"
        }
    ]
}
EOF
}
