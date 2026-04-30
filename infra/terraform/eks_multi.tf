provider "aws" {
  alias  = "us"
  region = "us-east-1"
}

provider "aws" {
  alias  = "ap"
  region = "ap-southeast-1"
}

module "eks_us" {
  source          = "terraform-aws-modules/eks/aws"
  providers       = { aws = aws.us }
  cluster_name    = "zeaz-us"
  cluster_version = "1.29"

  node_groups = {
    default = {
      desired_capacity = 3
      instance_types   = ["t3.large"]
    }
  }
}

module "eks_ap" {
  source          = "terraform-aws-modules/eks/aws"
  providers       = { aws = aws.ap }
  cluster_name    = "zeaz-ap"
  cluster_version = "1.29"

  node_groups = {
    default = {
      desired_capacity = 3
      instance_types   = ["t3.large"]
    }
  }
}
