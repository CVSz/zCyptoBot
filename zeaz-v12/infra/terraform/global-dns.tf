resource "aws_route53_record" "geo" {
  zone_id = var.zone
  name    = "zeaz.app"
  type    = "A"

  set_identifier = "region-a"
  geolocation_routing_policy {
    continent = "AS"
  }
}
