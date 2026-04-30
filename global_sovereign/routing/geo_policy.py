def route(user_region, data_type):
    if data_type == "PII":
        return user_region  # strict residency
    return "optimal"
