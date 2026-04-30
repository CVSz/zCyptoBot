from gid_standard.sdk.python.policy import PolicyEngine


def test_cross_border_pii_denied_by_default():
    p = PolicyEngine()
    claims = {"region": "eu-central-1"}
    assert p.evaluate(claims, resource_region="us-east-1", has_pii=True) is False


def test_same_region_pii_allowed():
    p = PolicyEngine()
    claims = {"region": "eu-central-1"}
    assert p.evaluate(claims, resource_region="eu-central-1", has_pii=True) is True
