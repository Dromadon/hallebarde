variable "env" {}

resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "hallebarde-${var.env}-database"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Name        = "hallebarde-${var.env}-database"
    Environment = "${var.env}"
  }
}
