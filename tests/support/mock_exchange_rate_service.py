from datetime import date
from decimal import Decimal
from typing import Literal

from app.models.currency_pair import CurrencyPair
from app.models.exchange_rate import ExchangeRate
from app.services.exchange_rate_service import ExchangeRateServiceInterface
from tests.support.factories import build_exchange_rate


class MockExchangeRateService(ExchangeRateServiceInterface):
    async def get_available_dates(self) -> list[date]:
        return [date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 3)]

    async def get_currency_pairs(self) -> list[CurrencyPair]:
        return [
            CurrencyPair(base_currency_code="USD", quote_currency_code="SGD"),
            CurrencyPair(base_currency_code="SGD", quote_currency_code="USD"),
            CurrencyPair(base_currency_code="USD", quote_currency_code="SGD"),
            CurrencyPair(base_currency_code="SGD", quote_currency_code="USD"),
            CurrencyPair(base_currency_code="EUR", quote_currency_code="JPY"),
            CurrencyPair(base_currency_code="JPY", quote_currency_code="EUR"),
            CurrencyPair(base_currency_code="EUR", quote_currency_code="USD"),
            CurrencyPair(base_currency_code="USD", quote_currency_code="EUR"),
            # Crypto
            CurrencyPair(base_currency_code="BTC", quote_currency_code="USD"),
            CurrencyPair(base_currency_code="USD", quote_currency_code="BTC"),
            # Unsupported currency
            CurrencyPair(
                base_currency_code="XYZ",
                quote_currency_code="USD",
            ),
            CurrencyPair(
                base_currency_code="USD",
                quote_currency_code="XYZ",
            ),
        ]

    async def get_latest_rate(
        self, base_currency_code: str, quote_currency_code: str, as_of: date | None = None
    ) -> ExchangeRate | None:
        if as_of is None:
            as_of = date.today()

        if base_currency_code == quote_currency_code:
            return build_exchange_rate(
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal(1),
                as_of=as_of,
            )[0]
        elif base_currency_code == "USD" and quote_currency_code == "EUR":
            return build_exchange_rate(
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal(1.02),
                as_of=as_of,
            )[0]

        return None

    async def get_historical_rates(
        self,
        base_currency_code: str,
        quote_currency_code: str,
        start_date: date | None = None,
        limit: int | None = None,
        sort_order: Literal["asc", "desc"] = "asc",
    ) -> list[ExchangeRate]:
        rates = [
            ExchangeRate(
                date=date(2024, 1, 1),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal(1),
            ),
            ExchangeRate(
                date=date(2024, 1, 2),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal(1.02),
            ),
            ExchangeRate(
                date=date(2024, 1, 3),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal(1.04),
            ),
        ]

        if start_date is not None:
            rates = [rate for rate in rates if rate.date >= start_date]

        if limit is not None:
            rates = rates[:limit]

        if sort_order == "desc":
            rates.reverse()

        return rates
