class EUInference:
    """
    Ensures inference runs only in EU region.
    """

    def run(self, model, x, region):
        if not region.startswith("eu"):
            raise PermissionError("non-EU execution blocked")
        return model(x)
