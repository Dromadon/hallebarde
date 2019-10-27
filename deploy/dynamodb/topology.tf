variable "env" {}

resource "aws_dynamodb_table" "hallebarde-table" {
  name           = "hallebarde-${var.env}-table"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "identifier"

  attribute {
    name = "identifier"
    type = "S"
  }

  tags = {
    Name        = "hallebarde-${var.env}-table"
    Environment = "${var.env}"
  }
}
