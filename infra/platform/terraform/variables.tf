variable "environment" { type = string }
variable "region" { type = string }
variable "cluster_name" { type = string }
variable "node_count" { type = number default = 3 }
variable "node_instance_type" { type = string default = "c3.large" }
variable "enable_ha_control_plane" { type = bool default = true }
