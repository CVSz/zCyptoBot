resource "aws_iam_role" "enterprise_admin" {
  name = "zeaz-enterprise-admin"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Sid    = "AllowCrossAccountFromOrg",
      Effect = "Allow",
      Principal = {
        AWS = "arn:aws:iam::*:root"
      },
      Action = "sts:AssumeRole",
      Condition = {
        StringEquals = {
          "aws:PrincipalOrgID" = aws_organizations_organization.org.id
        },
        Bool = {
          "aws:MultiFactorAuthPresent" = "true"
        }
      }
    }]
  })

  tags = {
    ManagedBy = "terraform"
    Scope     = "enterprise"
  }
}

resource "aws_iam_role_policy_attachment" "enterprise_admin_access" {
  role       = aws_iam_role.enterprise_admin.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}
