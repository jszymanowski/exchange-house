from datetime import date, timedelta
from decimal import Decimal
from typing import Literal, TypedDict

from tortoise.backends.base.client import BaseDBAsyncClient

from app.decorators.database_transactional import database_transactional
from app.models import Currency, CurrencyPair, ExchangeRate


class CreateRateParams(TypedDict):
    as_of: date
    base_currency_code: Currency
    quote_currency_code: Currency
    rate: Decimal
    source: str


class ExchangeRateServiceInterface:
    class Meta:
        abstract = True

    async def get_available_dates(self) -> list[date]:
        raise RuntimeError("Must be implemented")

    async def get_currency_pairs(self) -> list[CurrencyPair]:
        raise RuntimeError("Must be implemented")

    async def get_latest_rate(
        self, base_currency_code: Currency, quote_currency_code: Currency, as_of: date | None = None
    ) -> ExchangeRate | None:
        raise RuntimeError("Must be implemented")

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
        raise RuntimeError("Must be implemented")

    async def bulk_create_rates(self, params_set: list[CreateRateParams]) -> None:
        raise RuntimeError("Must be implemented")

    async def create_rate(
        self, as_of: date, base_currency_code: Currency, quote_currency_code: Currency, rate: Decimal, source: str
    ) -> list[ExchangeRate]:
        raise RuntimeError("Must be implemented")


class ExchangeRateService(ExchangeRateServiceInterface):
    async def get_available_dates(self) -> list[date]:
        distinct_dates = await ExchangeRate.all().distinct().order_by("as_of").values("as_of")
        return [d["as_of"] for d in distinct_dates]

    async def get_currency_pairs(self) -> list[CurrencyPair]:
        distinct_pairs = (
            await ExchangeRate.all()
            .distinct()
            .order_by("base_currency_code", "quote_currency_code")
            .values("base_currency_code", "quote_currency_code")
        )

        valid_pairs = []
        for pair in distinct_pairs:
            try:
                valid_pairs.append(CurrencyPair(**pair))
            except ValueError:
                # Skip invalid currency pairs
                continue

        return valid_pairs

    async def get_latest_rate(
        self, base_currency_code: Currency, quote_currency_code: Currency, as_of: date | None = None
    ) -> ExchangeRate | None:
        if as_of is None:
            as_of = date.today()

        if base_currency_code == quote_currency_code:
            return ExchangeRate(
                rate=Decimal("1.00000000"),
                as_of=as_of,
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
            )

        exchange_rate = (
            await ExchangeRate.filter(
                base_currency_code=base_currency_code,
                quote_currency_code=quote_currency_code,
                as_of__lte=as_of,
            )
            .order_by("-as_of")
            .first()
        )

        return exchange_rate

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
        if end_date is None:
            end_date = date.today()

        if start_date is None:
            start_date = end_date - timedelta(days=365.25 * 10)

        if start_date > end_date:
            raise ValueError("start_date must be before or equal to today")

        query_unlimited = ExchangeRate.filter(
            base_currency_code=base_currency_code,
            quote_currency_code=quote_currency_code,
            as_of__lte=end_date,
            as_of__gte=start_date,
        )

        query = query_unlimited

        if limit is not None:
            query = query.limit(limit)

        if offset is not None:
            query = query.offset(offset)

        if sort_order == "desc":
            query = query.order_by("-as_of")
        else:
            query = query.order_by("as_of")

        data = await query.all()
        total = await query_unlimited.count()

        return data, total

    @database_transactional
    async def bulk_create_rates(
        self, params_set: list[CreateRateParams], db_connection: BaseDBAsyncClient | None = None
    ) -> None:
        for params in params_set:
            await self.create_rate(**params, db_connection=db_connection)

    @database_transactional
    async def create_rate(
        self,
        as_of: date,
        base_currency_code: Currency,
        quote_currency_code: Currency,
        rate: Decimal,
        source: str,
        db_connection: BaseDBAsyncClient | None = None,
    ) -> list[ExchangeRate]:
        if base_currency_code == quote_currency_code:
            return []

        forward_rate = ExchangeRate(
            base_currency_code=base_currency_code,
            quote_currency_code=quote_currency_code,
            rate=rate,
            as_of=as_of,
            data_source=source,
        )
        inverse_rate = ExchangeRate(
            base_currency_code=quote_currency_code,
            quote_currency_code=base_currency_code,
            rate=1 / rate,
            as_of=as_of,
            data_source=source,
        )

        try:
            await forward_rate.save(using_db=db_connection)
            await inverse_rate.save(using_db=db_connection)
        except Exception as e:
            raise ValueError(
                f"Failed to create exchange rate for {base_currency_code} to "
                f"{quote_currency_code} on {as_of} with error {e}"
            ) from e

        return [forward_rate, inverse_rate]
