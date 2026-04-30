def allow(src_region, dst_region, data_class):
    if data_class == "PII" and src_region != dst_region:
        return False
    return True
