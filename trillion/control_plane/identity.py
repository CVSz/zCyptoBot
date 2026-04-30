class Identity:
    """Minimal zero-trust identity placeholder."""

    def __init__(self):
        self._tokens = {}

    def issue(self, principal: str, token: str) -> None:
        self._tokens[principal] = token

    def verify(self, principal: str, token: str) -> bool:
        return self._tokens.get(principal) == token
