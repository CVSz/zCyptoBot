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

module "network_primary" {
  source = "./modules/network"
  cidr   = var.primary_cidr
  region = var.primary_region
}

module "network_secondary" {
  source = "./modules/network"
  providers = { aws = aws.secondary }
  cidr   = var.secondary_cidr
  region = var.secondary_region
}
