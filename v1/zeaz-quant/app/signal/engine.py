class SignalEngine:
    def generate(self, features: dict) -> str:
        if (
            features["vol"] > 0.003
            and features["momentum"] > 0
            and features["oi"] > 1200
        ):
            return "LONG"

        if (
            features["vol"] > 0.003
            and features["momentum"] < 0
            and features["oi"] > 1200
        ):
            return "SHORT"

        return "HOLD"
