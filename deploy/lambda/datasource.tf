variable "env" {}

data "aws_iam_role" "role_s3" {
  name = "hallebarde-${var.env}-lambda-s3"
}

data "aws_iam_role" "role_basic" {
  name = "hallebarde-${var.env}-lambda-basic"
}
