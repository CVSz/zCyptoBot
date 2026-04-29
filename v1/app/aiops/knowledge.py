RULES = {
    "latency": ["scale_api", "restart_pods"],
    "error_rate": ["rollback_deploy", "restart_pods"],
    "kafka_lag": ["scale_consumers", "restart_kafka"],
}
