resource "aws_api_gateway_rest_api" "api" {
  name = "hallebarde-${var.env}"
  description = "This is my API for demonstration purposes"
}

resource "aws_api_gateway_deployment" "deployment" {
  depends_on = [
    aws_api_gateway_integration.s3_presigned_download_url,
    aws_api_gateway_integration.s3_presigned_upload_url,
    aws_api_gateway_integration.create_exchange,
    aws_api_gateway_integration.account_exchanges_integration]

  rest_api_id = aws_api_gateway_rest_api.api.id
  stage_name = var.env
  variables = {
    deployed_at = timestamp()
  }

  # This is mandatory for the name mapping not to fail during deployment
  # It creates the new deployment and switches the custom domain name mapping to it before deletion of the previous one
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_domain_name" "domain_name" {
  certificate_arn = data.aws_acm_certificate.cert.arn
  domain_name = "${var.env}.api.${var.route53_zone_name}"
}

resource "aws_route53_record" "example" {
  name = aws_api_gateway_domain_name.domain_name.domain_name
  type = "A"
  zone_id = data.aws_route53_zone.zone.id

  alias {
    evaluate_target_health = true
    name = aws_api_gateway_domain_name.domain_name.cloudfront_domain_name
    zone_id = aws_api_gateway_domain_name.domain_name.cloudfront_zone_id
  }
}

resource "aws_api_gateway_base_path_mapping" "test" {
  api_id = aws_api_gateway_rest_api.api.id
  stage_name = aws_api_gateway_deployment.deployment.stage_name
  domain_name = aws_api_gateway_domain_name.domain_name.domain_name
}