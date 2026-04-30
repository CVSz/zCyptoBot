def bind(token_hash: str, tls_session_id: str) -> str:
    return f"{token_hash}:{tls_session_id}"
