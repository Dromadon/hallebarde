resource "aws_iam_role_policy_attachment" "lambda_s3_presigned_url_attachment" {
  role       = aws_iam_role.lambda_role_s3.name
  policy_arn = aws_iam_policy.s3_managing_policy.arn
}

resource "aws_iam_role_policy_attachment" "lambda_s3_dynamodb" {
  role       = aws_iam_role.lambda_role_s3.name
  policy_arn = aws_iam_policy.dynamodb.arn
}

resource "aws_iam_role_policy_attachment" "lambda_s3_logging" {
  role       = aws_iam_role.lambda_role_s3.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

resource "aws_iam_role" "lambda_role_s3" {
  name               = "${var.application_name}-${var.env}-lambda-s3"
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

