import pytest

from revenue.billing.pricing import price


def test_price_sums_supported_metrics():
    usage = [
        {"metric": "cpu", "value": 10},
        {"metric": "gpu", "value": 2},
        {"metric": "request", "value": 1000},
    ]
    assert price(usage) == pytest.approx(2 * 0.5 + 10 * 0.02 + 1000 * 0.0001)


def test_price_rejects_unknown_metric():
    with pytest.raises(ValueError, match="Unsupported metric"):
        price([{"metric": "memory", "value": 1}])
