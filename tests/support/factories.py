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


def build_exchange_rate(**kwargs: ExchangeRateParams | dict) -> ExchangeRate:
    defaults = {
        "id": uuid.uuid4(),
        "as_of": date.today(),
        "base_currency_code": "USD",
        "quote_currency_code": "EUR",
        "rate": Decimal("0.85"),
        "data_source": "test",
    }

    # # Override defaults with any kwargs provided
    # defaults.update(kwargs)

    return ExchangeRate(**(defaults | kwargs))
