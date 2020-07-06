resource "aws_cloudwatch_event_rule" "revoke_exchanges" {
  name = "${var.application_name}-revoke-expired-exchanges-schedule"
  description = "Triggers revocation of expired exchanges on a regular basis"

  schedule_expression = "rate(1 day)"
}

resource "aws_cloudwatch_event_target" "revoke_lambda" {
  rule = aws_cloudwatch_event_rule.revoke_exchanges.name
  arn = data.aws_lambda_function.revoke_expired_exchanges.arn
}
