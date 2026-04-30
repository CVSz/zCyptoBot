from geo_conflicts.conflicts import conflict


def resolve(src, dst, data_type):
    if conflict(src, dst, data_type):
        if src == "EU":
            return "deny_or_localize"
        if dst == "US":
            return "anonymize_then_transfer"
        if dst == "APAC":
            return "local_processing_required"
    return "allow"
