resource "aws_vpc_endpoint" "s3" {
  vpc_id       = "vpc-eu-placeholder"
  service_name = "com.amazonaws.eu-central-1.s3"
}
