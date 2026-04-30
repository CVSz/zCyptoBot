provider "aws" {
  alias  = "eu"
  region = "eu-central-1"
}

module "eks_eu" {
  source          = "terraform-aws-modules/eks/aws"
  providers       = { aws = aws.eu }
  cluster_name    = "zeaz-eu"
  cluster_version = "1.29"

  node_groups = {
    core = {
      desired_capacity = 4
      instance_types   = ["m6i.large"]
    }
  }

  vpc_config = {
    endpoint_private_access = true
    endpoint_public_access  = false
  }
}
