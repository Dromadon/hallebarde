resource "aws_route53_record" "website_record" {
  zone_id = data.aws_route53_zone.zone.id
  name    = var.env == "prod" ? var.route53_zone_name : "${var.env}.${var.route53_zone_name}"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.website_distribution.domain_name
    zone_id                = aws_cloudfront_distribution.website_distribution.hosted_zone_id
    evaluate_target_health = true
  }
}