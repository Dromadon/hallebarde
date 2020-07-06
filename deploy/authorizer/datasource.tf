variable "env" {}
variable "application_name" {}

data "aws_iam_role" "role" {
  name = "${var.application_name}-${var.env}-lambda-basic"
}
