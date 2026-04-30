resource "aws_vpc_endpoint" "s3" {
  vpc_id       = aws_vpc.gov.id
  service_name = "com.amazonaws.eu-west-1.s3"
}
