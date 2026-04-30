resource "aws_kms_key" "eu" {
  provider                 = aws.eu
  description              = "EU Sovereign Key"
  deletion_window_in_days  = 30
  enable_key_rotation      = true
}
