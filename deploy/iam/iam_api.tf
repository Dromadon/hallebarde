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
          "accounts.google.com:aud": "${var.google_oidc_application}"
        }
      }
    }
  ]
}
EOF
}


