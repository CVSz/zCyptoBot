resource "aws_route53_record" "global" {
  zone_id = var.zone_id
  name    = "api.zeaz.io"
  type    = "A"

  set_identifier = "us"
  latency_routing_policy {
    region = "us-east-1"
  }

  alias {
    name                   = module.eks_us.cluster_endpoint
    zone_id                = var.zone_id
    evaluate_target_health = true
  }
}
