def validate_bucket(bucket: dict) -> bool:
    if bucket.get("public", False):
        return False
    return bucket.get("encryption") in {"AES256", "aws:kms"}
