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
  region = var.management_region
}

variable "management_region" {
  type        = string
  description = "AWS region for Organization management operations"
  default     = "us-east-1"
}

resource "aws_organizations_organization" "org" {
  aws_service_access_principals = [
    "cloudtrail.amazonaws.com",
    "config.amazonaws.com",
    "guardduty.amazonaws.com",
    "securityhub.amazonaws.com"
  ]

  enabled_policy_types = [
    "SERVICE_CONTROL_POLICY",
    "TAG_POLICY"
  ]

  feature_set = "ALL"
}

resource "aws_organizations_organizational_unit" "security" {
  name      = "Security"
  parent_id = aws_organizations_organization.org.roots[0].id
}

resource "aws_organizations_organizational_unit" "shared_services" {
  name      = "SharedServices"
  parent_id = aws_organizations_organization.org.roots[0].id
}

resource "aws_organizations_organizational_unit" "workloads" {
  name      = "Workloads"
  parent_id = aws_organizations_organization.org.roots[0].id
}

resource "aws_organizations_account" "billing" {
  name      = "zeaz-billing"
  email     = "billing@zeaz.io"
  parent_id = aws_organizations_organization.org.roots[0].id
}

resource "aws_organizations_account" "prod" {
  name      = "zeaz-prod"
  email     = "prod@zeaz.io"
  parent_id = aws_organizations_organizational_unit.workloads.id
}

resource "aws_organizations_account" "staging" {
  name      = "zeaz-staging"
  email     = "staging@zeaz.io"
  parent_id = aws_organizations_organizational_unit.workloads.id
}
