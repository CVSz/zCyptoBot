provider "aws" { region = var.region }

resource "aws_instance" "zeaz" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = var.instance_type
  key_name      = var.key_name

  user_data = <<-EOF
#!/bin/bash
set -e
curl -sfL https://get.k3s.io | sh -
mkdir -p /home/ec2-user/.kube
cp /etc/rancher/k3s/k3s.yaml /home/ec2-user/.kube/config
chown ec2-user:ec2-user /home/ec2-user/.kube/config
  EOF

  tags = { Name = "zeaz-k3s" }
}

output "public_ip" {
  value = aws_instance.zeaz.public_ip
}
