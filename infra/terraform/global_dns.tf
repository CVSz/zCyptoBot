resource "aws_route53_record" "api" {
  zone_id = var.zone
  name    = "api.zeaz.io"
  type    = "A"

  set_identifier = "aws"
  latency_routing_policy {
    region = "us-east-1"
  }

  alias {
    name                   = module.eks.cluster_endpoint
    zone_id                = var.zone
    evaluate_target_health = true
  }
}
