class KillSwitch:
    def __init__(self):
        self._on = False

    def set(self, v: bool):
        self._on = v

    def is_on(self):
        return self._on
