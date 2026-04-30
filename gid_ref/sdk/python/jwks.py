JWKS = {"keys": []}


def publish(kid, pub):
    JWKS["keys"].append({"kid": kid, "pub": pub})


def get(kid):
    for k in JWKS["keys"]:
        if k["kid"] == kid:
            return k["pub"]
    raise KeyError("kid not found")
