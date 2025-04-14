import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import TypedDict

from app.models.exchange_rate import ExchangeRate


class ExchangeRateParams(TypedDict, total=False):
    id: uuid.UUID
    as_of: date
    base_currency_code: str
    quote_currency_code: str
    rate: Decimal
    data_source: str
    created_at: datetime | None
    updated_at: datetime | None


def build_exchange_rate(**kwargs: ExchangeRateParams | dict) -> tuple[ExchangeRate, ExchangeRate]:
    defaults = {
        "as_of": date.today(),
        "base_currency_code": "USD",
        "quote_currency_code": "EUR",
        "rate": Decimal("0.85"),
        "data_source": "test",
    }
    attributes = defaults | kwargs
    inverse_attributes = attributes | {
        "base_currency_code": attributes["quote_currency_code"],
        "quote_currency_code": attributes["base_currency_code"],
        "rate": Decimal("1") / attributes["rate"],
    }

    return ExchangeRate(**attributes), ExchangeRate(**inverse_attributes)
