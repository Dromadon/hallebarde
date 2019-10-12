data "aws_iam_role" "role" {
  name = "hallebarde-${var.env}-lambda-basic"
}
