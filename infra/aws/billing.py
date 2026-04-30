"""AWS Cost Explorer integration for enterprise billing analytics."""

from __future__ import annotations

from datetime import date
from typing import Any

import boto3

ce = boto3.client("ce")


def cost_usage(start: str, end: str, granularity: str = "DAILY") -> dict[str, Any]:
    """Return blended and unblended cost and usage for the given date range.

    Dates should be passed as YYYY-MM-DD and end date is exclusive, as required by
    Cost Explorer APIs.
    """
    return ce.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity=granularity,
        Metrics=["BlendedCost", "UnblendedCost", "UsageQuantity"],
        GroupBy=[{"Type": "DIMENSION", "Key": "LINKED_ACCOUNT"}],
    )


def current_month_to_date() -> dict[str, Any]:
    today = date.today()
    month_start = today.replace(day=1)
    return cost_usage(month_start.isoformat(), today.isoformat())
