variable "cloudflare_api_token" {
  description = "Cloudflare API token scoped to DNS edit for the zeaz.dev zone."
  type        = string
  sensitive   = true
}

variable "zone_name" {
  description = "Root zone to manage."
  type        = string
  default     = "zeaz.dev"
}

variable "gateway_ipv4" {
  description = "Ingress gateway IPv4 target for wildcard DNS."
  type        = string
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "prod"
}
