data "aws_lambda_function" "revoke_expired_exchanges" {
  function_name = "${var.application_name}-${var.env}-revoke-expired-exchanges"
}
