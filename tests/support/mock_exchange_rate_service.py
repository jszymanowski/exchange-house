from datetime import date
from decimal import Decimal
from typing import Literal

from app.models import Currency, CurrencyPair, ExchangeRate
from app.services.exchange_rate_service import ExchangeRateServiceInterface
from tests.support.factories import build_exchange_rate


class MockExchangeRateService(ExchangeRateServiceInterface):
    async def get_available_dates(self) -> list[date]:
        return [date(2025, 4, 1), date(2025, 4, 2), date(2025, 4, 3)]

    async def get_currency_pairs(self) -> list[CurrencyPair]:
        return [
            CurrencyPair(base_currency_code="EUR", quote_currency_code="USD"),
            CurrencyPair(base_currency_code="GBP", quote_currency_code="USD"),
            CurrencyPair(base_currency_code="JPY", quote_currency_code="USD"),
            CurrencyPair(base_currency_code="SGD", quote_currency_code="USD"),
            CurrencyPair(base_currency_code="USD", quote_currency_code="EUR"),
            CurrencyPair(base_currency_code="USD", quote_currency_code="GBP"),
            CurrencyPair(base_currency_code="USD", quote_currency_code="JPY"),
            CurrencyPair(base_currency_code="USD", quote_currency_code="SGD"),
        ]

    async def get_latest_rate(
        self, base_currency_code: Currency, quote_currency_code: Currency, as_of: date | None = None
    ) -> ExchangeRate | None:
        if as_of is None:
            as_of = date.today()

        if base_currency_code == quote_currency_code:
            return build_exchange_rate(
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal(1),
                as_of=as_of,
            )
        elif base_currency_code == "USD" and quote_currency_code == "EUR":
            return build_exchange_rate(
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal(1.02),
                as_of=as_of,
            )
        elif base_currency_code == "USD" and quote_currency_code == "GBP":
            return build_exchange_rate(
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal(1.09),
                as_of=as_of,
            )

        return None

    async def get_historical_rates(
        self,
        base_currency_code: Currency,
        quote_currency_code: Currency,
        start_date: date | None = None,
        end_date: date | None = None,
        limit: int | None = None,
        sort_order: Literal["asc", "desc"] = "asc",
    ) -> list[ExchangeRate]:
        rates = [
            build_exchange_rate(
                as_of=date(2024, 1, 1),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal(1),
            ),
            build_exchange_rate(
                as_of=date(2024, 1, 2),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal(1.02),
            ),
            build_exchange_rate(
                as_of=date(2024, 1, 3),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal(1.04),
            ),
            build_exchange_rate(
                as_of=date(2024, 1, 5),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal(1.05),
            ),
            build_exchange_rate(
                as_of=date(2024, 4, 2),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal(1.12),
            ),
            build_exchange_rate(
                as_of=date(2024, 10, 10),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal(0.98),
            ),
            build_exchange_rate(
                as_of=date(2024, 10, 22),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal(0.95),
            ),
            build_exchange_rate(
                as_of=date(2024, 10, 31),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal(0.92),
            ),
        ]

        if start_date is not None:
            rates = [rate for rate in rates if rate.as_of >= start_date]

        if end_date is not None:
            rates = [rate for rate in rates if rate.as_of <= end_date]

        if limit is not None:
            rates = rates[:limit]

        if sort_order == "desc":
            rates.reverse()

        return rates
