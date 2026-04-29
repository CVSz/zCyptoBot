resource "aws_eks_node_group" "spot" {
  cluster_name    = var.cluster
  node_group_name = "spot-ng"
  capacity_type   = "SPOT"

  scaling_config {
    desired_size = 2
    max_size     = 10
    min_size     = 1
  }
}
