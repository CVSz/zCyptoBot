def map_to_entra(claims):
    return {"principal": claims["sub"]}
