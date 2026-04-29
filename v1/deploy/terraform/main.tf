terraform {
  required_version = ">= 1.6.0"
}

module "trading_stack" {
  source = "./modules/trading_stack"

  namespace = "trading"
  kafka_brokers = 3
  redis_replicas = 3
  rl_node_group_size = 4
}
