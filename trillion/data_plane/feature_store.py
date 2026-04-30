class FeatureStore:
    """
    Online/offline feature parity with simple cache.
    """

    def __init__(self):
        self.online = {}
        self.offline = {}

    def upsert(self, key: str, feats: dict):
        self.online[key] = feats
        self.offline[key] = feats

    def get(self, key: str) -> dict:
        return self.online.get(key, {})
