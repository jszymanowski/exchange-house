from pydantic import BaseModel


class CurrencyPairResponse(BaseModel):
    """Response model for currency pair data."""

    base_currency_code: str
    """ISO code for the source currency."""

    quote_currency_code: str
    """ISO code for the target currency."""
