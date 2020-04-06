resource "aws_acm_certificate" "website_certificate" {
  domain_name       = "${var.env}.${var.route53_zone_name}"
  validation_method = "DNS"

  tags = {
    Environment = var.env
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "website_certificate_validation_record" {
  name    = aws_acm_certificate.website_certificate.domain_validation_options[0].resource_record_name
  type    = aws_acm_certificate.website_certificate.domain_validation_options[0].resource_record_type
  zone_id = data.aws_route53_zone.zone.id
  records = [aws_acm_certificate.website_certificate.domain_validation_options[0].resource_record_value]
  ttl     = 60
}

resource "aws_acm_certificate_validation" "website_certificate_validation" {
  certificate_arn         = aws_acm_certificate.website_certificate.arn
  validation_record_fqdns = [aws_route53_record.website_certificate_validation_record.fqdn]
}