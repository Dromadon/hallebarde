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
  role       = "${aws_iam_role.lambda_role_s3.name}"
  policy_arn = "${aws_iam_policy.s3_presigned_urls_policy.arn}"
}

resource "aws_iam_role" "lambda_role_s3" {
  name = "hallebarde-${var.env}-lambda-s3"
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

