KEYS = {"active_kid": "k1", "keys": {"k1": "pub1"}}


def rotate(new_kid: str, pub: str):
    KEYS["keys"][new_kid] = pub
    KEYS["active_kid"] = new_kid
    return KEYS["active_kid"]
