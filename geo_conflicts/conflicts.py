def conflict(src, dst, data_type):
    if data_type == "PII" and src != dst:
        return True
    return False
