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
            CurrencyPair(base_currency_code=Currency("EUR"), quote_currency_code=Currency("USD")),
            CurrencyPair(base_currency_code=Currency("GBP"), quote_currency_code=Currency("USD")),
            CurrencyPair(base_currency_code=Currency("JPY"), quote_currency_code=Currency("USD")),
            CurrencyPair(base_currency_code=Currency("SGD"), quote_currency_code=Currency("USD")),
            CurrencyPair(base_currency_code=Currency("USD"), quote_currency_code=Currency("EUR")),
            CurrencyPair(base_currency_code=Currency("USD"), quote_currency_code=Currency("GBP")),
            CurrencyPair(base_currency_code=Currency("USD"), quote_currency_code=Currency("JPY")),
            CurrencyPair(base_currency_code=Currency("USD"), quote_currency_code=Currency("SGD")),
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
                rate=Decimal("1.00000000"),
                as_of=as_of,
            )
        elif base_currency_code == Currency("USD") and quote_currency_code == Currency("EUR"):
            return build_exchange_rate(
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal("1.02000000"),
                as_of=as_of,
            )
        elif base_currency_code == Currency("USD") and quote_currency_code == Currency("GBP"):
            return build_exchange_rate(
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal("1.09000000"),
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
        offset: int | None = None,
        sort_order: Literal["asc", "desc"] = "asc",
    ) -> tuple[list[ExchangeRate], int]:
        rates = [
            build_exchange_rate(
                as_of=date(2024, 1, 1),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal("1.00000000"),
            ),
            build_exchange_rate(
                as_of=date(2024, 1, 2),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal("1.02000000"),
            ),
            build_exchange_rate(
                as_of=date(2024, 1, 3),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal("1.04000000"),
            ),
            build_exchange_rate(
                as_of=date(2024, 1, 5),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal("1.05000000"),
            ),
            build_exchange_rate(
                as_of=date(2024, 4, 2),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal("1.12000000"),
            ),
            build_exchange_rate(
                as_of=date(2024, 10, 10),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal("0.98000000"),
            ),
            build_exchange_rate(
                as_of=date(2024, 10, 22),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal("0.95000000"),
            ),
            build_exchange_rate(
                as_of=date(2024, 10, 31),
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                rate=Decimal("0.92000000"),
            ),
        ]
        total = len(rates)

        if start_date is not None:
            rates = [rate for rate in rates if rate.as_of >= start_date]

        if end_date is not None:
            rates = [rate for rate in rates if rate.as_of <= end_date]

        if offset is not None:
            rates = rates[offset:]

        if limit is not None:
            rates = rates[:limit]

        if sort_order == "desc":
            rates.reverse()

        return rates, total
