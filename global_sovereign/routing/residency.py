def allow(src, dst, data_type):
    if data_type == "PII" and src != dst:
        return False
    return True
