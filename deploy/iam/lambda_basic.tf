resource "aws_iam_policy" "dynamodb" {
  name        = "hallebarde-${var.env}-dynamodb"
  description = "Allows hallebarde to access dynamodb"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:*"
            ],
            "Resource": "${data.aws_dynamodb_table.table.arn}"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_get_token_attachment" {
  role       = "${aws_iam_role.lambda_role_basic.name}"
  policy_arn = "${aws_iam_policy.dynamodb.arn}"
}

resource "aws_iam_role" "lambda_role_basic" {
  name = "hallebarde-${var.env}-lambda-basic"

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
