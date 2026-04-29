output "primary_region" { value = var.primary_region }
output "secondary_region" { value = var.secondary_region }
output "primary_server_public_ip" { value = aws_instance.k3s_server_primary.public_ip }
output "secondary_server_public_ip" { value = aws_instance.k3s_server_secondary.public_ip }
