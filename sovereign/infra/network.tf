resource "aws_vpc" "eu" {
  provider             = aws.eu
  cidr_block           = "10.60.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "zeaz-eu-vpc"
    Sovereignty = "eu-only"
  }
}

resource "aws_security_group" "private_only" {
  provider = aws.eu
  name     = "zeaz-eu-private-only"
  vpc_id   = aws_vpc.eu.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_vpc.eu.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_vpc.eu.cidr_block]
  }
}
