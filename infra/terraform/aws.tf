provider "aws" {
  region = "us-east-1"
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "zeaz-aws"
  cluster_version = "1.29"

  node_groups = {
    default = {
      desired_capacity = 5
      instance_types   = ["m5.large"]
    }
  }
}
