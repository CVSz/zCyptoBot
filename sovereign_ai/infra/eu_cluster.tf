provider "aws" {
  region = "eu-central-1"
}

resource "aws_instance" "gpu" {
  ami           = "ami-gpu-eu"
  instance_type = "p4d.24xlarge"
  count         = 2
}
