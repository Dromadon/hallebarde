variable "env" {}

resource "aws_iam_policy" "s3_presigned_urls_role" {
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

resource "aws_iam_role" "api_authent_role" {
  name = "hallebarde-${var.env}-api-authent"
  path = "/hallebarde/"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "accounts.google.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "accounts.google.com:aud": "274210205449-bend56f57m2gcu9an3q6dmv0atj3i7h1.apps.googleusercontent.com"
        }
      }
    }
  ]
}
EOF
}
