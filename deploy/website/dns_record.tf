resource "aws_route53_record" "website_record" {
  zone_id = data.aws_route53_zone.zone.id
  name    = "${var.env}.${var.route53_zone_name}"
  type    = "CNAME"
  ttl     = "300"
  records = [aws_cloudfront_distribution.website_distribution.domain_name]
}