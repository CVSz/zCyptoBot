def evaluate(resource: dict) -> dict:
    return {
        "encryption": resource.get("encryption") == "AES256",
        "auth": resource.get("auth") in ["OIDC", "mTLS"],
        "logging": resource.get("logging") is True,
    }
