output "primary_public_subnet_id" { value = aws_subnet.primary_public.id }
output "secondary_public_subnet_id" { value = aws_subnet.secondary_public.id }
output "primary_k3s_sg_id" { value = aws_security_group.primary_k3s.id }
output "secondary_k3s_sg_id" { value = aws_security_group.secondary_k3s.id }
