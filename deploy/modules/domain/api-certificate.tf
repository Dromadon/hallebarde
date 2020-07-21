resource "aws_acm_certificate" "api_certificate" {
  domain_name       = "${var.env == "prod" ? "" : "${var.env}."}api.${var.route53_zone_name}"
  validation_method = "DNS"

  tags = {
    Environment = var.env
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "api_certificate_validation_record" {
  name    = aws_acm_certificate.api_certificate.domain_validation_options[0].resource_record_name
  type    = aws_acm_certificate.api_certificate.domain_validation_options[0].resource_record_type
  zone_id = data.aws_route53_zone.zone.id
  records = [aws_acm_certificate.api_certificate.domain_validation_options[0].resource_record_value]
  ttl     = 60
}

resource "aws_acm_certificate_validation" "api_certificate_validation" {
  certificate_arn         = aws_acm_certificate.api_certificate.arn
  validation_record_fqdns = [aws_route53_record.api_certificate_validation_record.fqdn]
}