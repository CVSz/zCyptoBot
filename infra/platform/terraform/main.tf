terraform {
  required_version = ">= 1.7.0"
}

locals {
  labels = {
    platform    = "zeaz"
    environment = var.environment
    region      = var.region
  }
}

# Provider-specific cluster modules should be wired here (AWS/GCP/Azure/bare-metal).
# This root module intentionally exposes a stable interface so environments can swap
# substrate providers without changing GitOps application definitions.

output "cluster_contract" {
  value = {
    cluster_name            = var.cluster_name
    environment             = var.environment
    region                  = var.region
    node_count              = var.node_count
    enable_ha_control_plane = var.enable_ha_control_plane
    required_addons         = ["cert-manager", "external-dns", "argo-cd", "vault", "spire", "istio", "otel-collector"]
    labels                  = local.labels
  }
}
