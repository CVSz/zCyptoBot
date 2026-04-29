variable "cidr" { type = string }
variable "region" { type = string }
resource "aws_vpc" "this" {
  cidr_block = var.cidr
  tags = { Name = "zcyptobot-${var.region}-vpc" }
}
