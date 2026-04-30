from geo_policy import allow


def transfer(data, src, dst, data_class):
    if not allow(src, dst, data_class):
        raise PermissionError("cross-border PII blocked")
    return {"moved": True, "dst": dst}
