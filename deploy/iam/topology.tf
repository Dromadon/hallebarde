variable "env" {}

resource "aws_iam_policy" "s3_presigned_urls_policy" {
  name        = "hallebarde-${var.env}-s3-presigned-url"
  description = "Allows hallebarde to create s3 presigned urls in hallebarde bucket"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
{
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:*"
            ],
            "Resource": "${data.aws_s3_bucket.bucket.arn}/*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_s3_presigned_url_attachment" {
  role       = "${aws_iam_role.lambda_role.name}"
  policy_arn = "${aws_iam_policy.s3_presigned_urls_policy.arn}"
}

resource "aws_iam_role" "api_authent_role" {
  name = "hallebarde-${var.env}-api-authent"
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

resource "aws_iam_role" "lambda_role" {
  name = "hallebarde-${var.env}-lambda"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

