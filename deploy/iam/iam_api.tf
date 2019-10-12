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


