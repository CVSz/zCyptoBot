terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.primary_region
}

provider "aws" {
  alias  = "secondary"
  region = var.secondary_region
}

module "network" {
  source = "./modules/network"

  providers = {
    aws           = aws
    aws.secondary = aws.secondary
  }

  primary_region   = var.primary_region
  secondary_region = var.secondary_region
  primary_cidr     = var.primary_cidr
  secondary_cidr   = var.secondary_cidr
}

resource "aws_instance" "k3s_server_primary" {
  ami           = var.ami_id
  instance_type = var.k3s_server_instance_type
  subnet_id     = module.network.primary_public_subnet_id
  key_name      = var.ssh_key_name

  vpc_security_group_ids = [module.network.primary_k3s_sg_id]

  user_data = templatefile("${path.module}/templates/k3s-server.sh.tftpl", {
    cluster_token = var.k3s_cluster_token
    node_label    = "region=primary"
  })

  tags = {
    Name = "zcyptobot-k3s-primary-server"
    Role = "k3s-server"
  }
}

resource "aws_instance" "k3s_server_secondary" {
  provider      = aws.secondary
  ami           = var.ami_id
  instance_type = var.k3s_server_instance_type
  subnet_id     = module.network.secondary_public_subnet_id
  key_name      = var.ssh_key_name

  vpc_security_group_ids = [module.network.secondary_k3s_sg_id]

  user_data = templatefile("${path.module}/templates/k3s-server.sh.tftpl", {
    cluster_token = var.k3s_cluster_token
    node_label    = "region=secondary"
  })

  tags = {
    Name = "zcyptobot-k3s-secondary-server"
    Role = "k3s-server"
  }
}
