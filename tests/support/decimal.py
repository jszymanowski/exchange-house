from decimal import ROUND_HALF_UP, Decimal


def quantize_decimal(value: str | int | float | Decimal) -> Decimal:
    """Helper function to round Decimal values consistently for comparison."""
    return Decimal(value).quantize(Decimal("0.000000001"), rounding=ROUND_HALF_UP)
