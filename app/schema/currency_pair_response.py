from pydantic import BaseModel


class CurrencyPairResponse(BaseModel):
    """Response model for currency pair data."""

    from_iso_code: str
    """ISO code for the source currency."""

    to_iso_code: str
    """ISO code for the target currency."""
