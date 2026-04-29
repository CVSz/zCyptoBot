from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SurveillanceAlert:
    rule: str
    severity: str
    message: str


class MarketSurveillance:
    """Simple controls for layering/spoofing-like behaviour detection."""

    def detect_quote_instability(self, add_rate: float, cancel_rate: float) -> list[SurveillanceAlert]:
        alerts: list[SurveillanceAlert] = []
        if add_rate > 10 and cancel_rate / max(add_rate, 1e-6) > 0.85:
            alerts.append(
                SurveillanceAlert(
                    rule="QUOTE_INSTABILITY_001",
                    severity="high",
                    message="High quote add/cancel ratio detected; review strategy behavior.",
                )
            )
        return alerts
