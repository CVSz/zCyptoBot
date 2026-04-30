resource "aws_route53_record" "global" {
  name           = "api.gid"
  type           = "A"
  set_identifier = "latency"
}
