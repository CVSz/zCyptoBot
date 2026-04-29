import json
import os

cfg = {
    "env": {
        "KAFKA_BROKER": "kafka:9092",
        "REDIS_HOST": "redis",
        "VAULT_ADDR": "http://vault:8200"
    }
}

os.makedirs("generated", exist_ok=True)
with open("generated/config.json", "w", encoding="utf-8") as f:
    json.dump(cfg, f, indent=2)
    f.write("\n")
