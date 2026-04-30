class InferenceService:
    def run(self, model, x):
        # wrap model call; add guards
        if not callable(model):
            raise TypeError("model not callable")
        return model(x)
