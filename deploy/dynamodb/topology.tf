variable "env" {}
variable "application_name" {}

resource "aws_dynamodb_table" "hallebarde-table" {
  name           = "${var.application_name}-${var.env}-table"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "identifier"

  attribute {
    name = "identifier"
    type = "S"
  }

  tags = {
    Name        = "${var.application_name}-${var.env}-table"
    Environment = "${var.env}"
  }
}
