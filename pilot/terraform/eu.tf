provider "aws" {
  alias  = "eu"
  region = "eu-central-1"
}

resource "aws_eks_cluster" "eu" {
  provider = aws.eu
  name     = "gid-eu"
}
