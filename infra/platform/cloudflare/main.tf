terraform {
  required_version = ">= 1.7.0"
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

data "cloudflare_zone" "zeaz" {
  name = var.zone_name
}

resource "cloudflare_record" "wildcard" {
  zone_id = data.cloudflare_zone.zeaz.id
  name    = "*"
  value   = var.gateway_ipv4
  type    = "A"
  proxied = true
  ttl     = 1
  comment = "Managed by ZeaZ GitOps platform for wildcard service routing."
}

resource "cloudflare_record" "environment_wildcard" {
  zone_id = data.cloudflare_zone.zeaz.id
  name    = "*.${var.environment}"
  value   = var.gateway_ipv4
  type    = "A"
  proxied = true
  ttl     = 1
  comment = "Managed by ZeaZ GitOps platform for environment-scoped dynamic routing."
}

resource "cloudflare_zone_settings_override" "secure_defaults" {
  zone_id = data.cloudflare_zone.zeaz.id
  settings {
    always_use_https         = "on"
    automatic_https_rewrites = "on"
    brotli                   = "on"
    min_tls_version          = "1.2"
    ssl                      = "strict"
    tls_1_3                  = "on"
  }
}
