"""Per-run Google Maps API usage and cost estimates.

The tracker is intentionally local: it cannot see calls made outside this
program or the billing account's authoritative monthly totals.
"""

from collections import Counter


GOOGLE_SKUS = {
    "Geocoding": {
        "free_cap": 10_000,
        "price_per_1000": 5.00,
    },
    "Places Nearby Search Pro": {
        "free_cap": 5_000,
        "price_per_1000": 32.00,
    },
}

_calls = Counter()


def reset_usage() -> None:
    _calls.clear()


def record_call(sku: str) -> None:
    _calls[sku] += 1


def build_usage_report(month_to_date: dict[str, int]) -> list[dict]:
    """Build report rows using optional pre-run monthly call totals."""
    rows = []
    for sku, pricing in GOOGLE_SKUS.items():
        before = month_to_date.get(sku, 0)
        current_run = _calls[sku]
        total = before + current_run
        paid_calls = max(0, total - pricing["free_cap"])
        estimated_cost = paid_calls * pricing["price_per_1000"] / 1000
        rows.append({
            "Google Maps SKU": sku,
            "Calls this run": current_run,
            "Configured month-to-date before run": before,
            "Projected monthly calls": total,
            "Monthly free-call cap": pricing["free_cap"],
            "Free calls remaining": max(0, pricing["free_cap"] - total),
            "Price after cap (USD / 1,000)": pricing["price_per_1000"],
            "Estimated cost after free cap (USD)": round(estimated_cost, 2),
        })
    return rows
