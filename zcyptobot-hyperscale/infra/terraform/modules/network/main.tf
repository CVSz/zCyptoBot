resource "aws_vpc" "primary" {
  cidr_block = var.primary_cidr
  tags = { Name = "zcyptobot-${var.primary_region}-vpc" }
}

resource "aws_vpc" "secondary" {
  provider   = aws.secondary
  cidr_block = var.secondary_cidr
  tags = { Name = "zcyptobot-${var.secondary_region}-vpc" }
}

resource "aws_subnet" "primary_public" {
  vpc_id                  = aws_vpc.primary.id
  cidr_block              = cidrsubnet(var.primary_cidr, 8, 1)
  map_public_ip_on_launch = true
  tags = { Name = "zcyptobot-primary-public" }
}

resource "aws_subnet" "secondary_public" {
  provider                = aws.secondary
  vpc_id                  = aws_vpc.secondary.id
  cidr_block              = cidrsubnet(var.secondary_cidr, 8, 1)
  map_public_ip_on_launch = true
  tags = { Name = "zcyptobot-secondary-public" }
}

resource "aws_security_group" "primary_k3s" {
  name   = "zcyptobot-primary-k3s-sg"
  vpc_id = aws_vpc.primary.id

  ingress { from_port = 22 to_port = 22 protocol = "tcp" cidr_blocks = ["0.0.0.0/0"] }
  ingress { from_port = 6443 to_port = 6443 protocol = "tcp" cidr_blocks = ["0.0.0.0/0"] }
  ingress { from_port = 8472 to_port = 8472 protocol = "udp" cidr_blocks = [var.primary_cidr, var.secondary_cidr] }

  egress { from_port = 0 to_port = 0 protocol = "-1" cidr_blocks = ["0.0.0.0/0"] }
}

resource "aws_security_group" "secondary_k3s" {
  provider = aws.secondary
  name     = "zcyptobot-secondary-k3s-sg"
  vpc_id   = aws_vpc.secondary.id

  ingress { from_port = 22 to_port = 22 protocol = "tcp" cidr_blocks = ["0.0.0.0/0"] }
  ingress { from_port = 6443 to_port = 6443 protocol = "tcp" cidr_blocks = ["0.0.0.0/0"] }
  ingress { from_port = 8472 to_port = 8472 protocol = "udp" cidr_blocks = [var.primary_cidr, var.secondary_cidr] }

  egress { from_port = 0 to_port = 0 protocol = "-1" cidr_blocks = ["0.0.0.0/0"] }
}
