data "aws_lambda_function" "revoke_expired_exchanges" {
  function_name = "hallebarde-${var.env}-revoke-expired-exchanges"
}