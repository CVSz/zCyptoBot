variable "primary_region" { default = "us-east-1" }
variable "secondary_region" { default = "us-west-2" }
variable "primary_cidr" { default = "10.10.0.0/16" }
variable "secondary_cidr" { default = "10.20.0.0/16" }

variable "ami_id" {
  description = "AMI with Ubuntu 22.04+"
  type        = string
}

variable "ssh_key_name" {
  description = "EC2 key pair name"
  type        = string
}

variable "k3s_server_instance_type" {
  type    = string
  default = "t3.large"
}

variable "k3s_cluster_token" {
  description = "Shared token for k3s cluster nodes"
  type        = string
  sensitive   = true
}
