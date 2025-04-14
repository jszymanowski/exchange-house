from datetime import date
from decimal import Decimal
from typing import Literal

from app.models.exchange_rate import CurrencyPair, ExchangeRate
from app.models.exchange_rate_service import ExchangeRateServiceInterface


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
        if base_currency_code == quote_currency_code:
            return ExchangeRate(
                rate=Decimal(1),
                date=date(2024, 1, 1),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
            )
        elif base_currency_code == "USD" and quote_currency_code == "SGD":
            return ExchangeRate(
                rate=Decimal(1.3333333333333333),
                date=date(2024, 1, 1),
                base_currency_code="USD",
                quote_currency_code="SGD",
            )
        elif base_currency_code == "SGD" and quote_currency_code == "USD":
            return ExchangeRate(
                rate=Decimal(0.75),
                date=date(2024, 1, 1),
                base_currency_code="SGD",
                quote_currency_code="USD",
            )
        elif base_currency_code == "USD" and quote_currency_code == "USD":
            return ExchangeRate(
                rate=Decimal(1),
                date=date(2024, 1, 1),
                base_currency_code="USD",
                quote_currency_code="USD",
            )
        elif base_currency_code == "SGD" and quote_currency_code == "SGD":
            return ExchangeRate(
                rate=Decimal(1),
                date=date(2024, 1, 1),
                base_currency_code="SGD",
                quote_currency_code="SGD",
            )
        elif base_currency_code == "THB" and quote_currency_code == "USD":
            return ExchangeRate(
                rate=Decimal(0.03),
                date=date(2025, 1, 1),
                base_currency_code="THB",
                quote_currency_code="USD",
            )
        elif base_currency_code == "USD" and quote_currency_code == "THB":
            return ExchangeRate(
                rate=Decimal(33.33),
                date=date(2025, 1, 1),
                base_currency_code="USD",
                quote_currency_code="THB",
            )
        elif base_currency_code == "CAD" and quote_currency_code == "USD":
            return ExchangeRate(
                rate=Decimal(0.70),
                date=date(2024, 1, 1),
                base_currency_code="CAD",
                quote_currency_code="USD",
            )
        elif base_currency_code == "USD" and quote_currency_code == "CAD":
            return ExchangeRate(
                rate=Decimal(1.43),
                date=date(2024, 1, 1),
                base_currency_code="USD",
                quote_currency_code="CAD",
            )
        elif base_currency_code == "CUSTOM_AMEX" and quote_currency_code == "USD":
            return ExchangeRate(
                rate=Decimal(0.006),
                date=date(2024, 1, 1),
                base_currency_code="CUSTOM_AMEX",
                quote_currency_code="USD",
            )
        elif base_currency_code == "USD" and quote_currency_code == "CUSTOM_AMEX":
            return ExchangeRate(
                rate=Decimal(166.66666667),
                date=date(2024, 1, 1),
                base_currency_code="USD",
                quote_currency_code="CUSTOM_AMEX",
            )
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
