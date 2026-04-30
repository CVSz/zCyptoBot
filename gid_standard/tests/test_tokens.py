import base64
import json
import time

import pytest

from gid_standard.sdk.python.verifier import Verifier


def _enc(payload: dict) -> str:
    raw = json.dumps(payload, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def test_valid_token_passes():
    v = Verifier({"trusted"})
    token = _enc({"iss": "trusted", "exp": int(time.time()) + 60, "att": "abc", "jti": "1"})
    assert v.verify(token)["iss"] == "trusted"


def test_expired_rejected():
    v = Verifier({"trusted"})
    token = _enc({"iss": "trusted", "exp": int(time.time()) - 1, "att": "abc", "jti": "2"})
    with pytest.raises(ValueError, match="expired"):
        v.verify(token)


def test_untrusted_rejected():
    v = Verifier({"trusted"})
    token = _enc({"iss": "evil", "exp": int(time.time()) + 60, "att": "abc", "jti": "3"})
    with pytest.raises(ValueError, match="untrusted issuer"):
        v.verify(token)


def test_revoked_rejected():
    v = Verifier({"trusted"}, revoked_jti={"revoked-id"})
    token = _enc({"iss": "trusted", "exp": int(time.time()) + 60, "att": "abc", "jti": "revoked-id"})
    with pytest.raises(ValueError, match="revoked"):
        v.verify(token)
