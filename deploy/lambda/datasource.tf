variable "env" {}
variable "application_name" {}

data "aws_iam_role" "role_s3" {
  name = "${var.application_name}-${var.env}-lambda-s3"
}

data "aws_iam_role" "role_basic" {
  name = "${var.application_name}-${var.env}-lambda-basic"
}
