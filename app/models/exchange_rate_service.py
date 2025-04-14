from datetime import date
from decimal import Decimal
from typing import Literal

from app.models.currency_pair import CurrencyPair
from app.models.exchange_rate import ExchangeRate


class ExchangeRateServiceInterface:
    class Meta:
        abstract = True

    async def get_currency_pairs(self) -> list[CurrencyPair]:
        raise RuntimeError("Must be implemented")

    async def get_available_dates(self) -> list[date]:
        raise RuntimeError("Must be implemented")

    async def get_latest_rate(
        self, base_currency_code: str, quote_currency_code: str, as_of: date
    ) -> ExchangeRate | None:
        raise RuntimeError("Must be implemented")

    async def get_historical_rates(
        self,
        base_currency_code: str,
        quote_currency_code: str,
        start_date: date | None = None,
        limit: int | None = None,
        sort_order: Literal["asc", "desc"] = "asc",
    ) -> list[ExchangeRate]:
        raise RuntimeError("Must be implemented")

    async def create_rate(
        self, as_of: date, base_currency_code: str, quote_currency_code: str, rate: Decimal
    ) -> list[ExchangeRate]:
        raise RuntimeError("Must be implemented")


class ExchangeRateService(ExchangeRateServiceInterface):
    async def get_available_dates(self) -> list[date]:
        distinct_dates = await ExchangeRate.all().distinct().values("as_of")
        return [d["as_of"] for d in distinct_dates]

    async def get_currency_pairs(self) -> list[CurrencyPair]:
        distinct_pairs = (
            await ExchangeRate.all()
            .distinct()
            .order_by("base_currency_code", "quote_currency_code")
            .values("base_currency_code", "quote_currency_code")
        )
        return [CurrencyPair(**pair) for pair in distinct_pairs]

    async def get_latest_rate(
        self, base_currency_code: str, quote_currency_code: str, as_of: date
    ) -> ExchangeRate | None:
        if base_currency_code == quote_currency_code:
            return ExchangeRate(
                rate=Decimal(1),
                date=as_of,
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
            .get()
        )

        return exchange_rate

    # async def get_historical_rates(
    #     self,
    #     base_currency_code: str,
    #     quote_currency_code: str,
    #     start_date: Optional[date] = None,
    #     limit: Optional[int] = None,
    #     sort_order: Literal["asc", "desc"] = "asc",
    # ) -> list[ExchangeRate]:
    #     end_date = date.today()
    #     if start_date is None:
    #         start_date = end_date - timedelta(days=365.25 * 10)

    #     if start_date > end_date:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail="start_date must be before or equal to today",
    #         )

    #     if limit is None:
    #         limit = MAX_RECORDS_PER_REQUEST

    #     query = (
    #         self.exchange_house.table(self.table)
    #         .select("rate, date")
    #         .eq("base_currency", base_currency_code)
    #         .eq("target_currency", quote_currency_code)
    #         .gte("date", start_date.isoformat())
    #         .lte("date", end_date.isoformat())
    #         .order("date", desc=(sort_order == "desc"))
    #         .limit(limit)
    #     )

    #     response = query.execute()
    #     all_rates = response.data

    #     if not all_rates:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f"No exchange rates found for {base_currency_code}"
    #             f" to {quote_currency_code} between {start_date} and {end_date}",
    #         )

    #     if len(all_rates) == MAX_RECORDS_PER_REQUEST:
    #         logger.warning(f"Reached the maximum number of records per request: {MAX_RECORDS_PER_REQUEST}")

    #     return [
    #         self._parse_response(data=rate, base_currency_code=base_currency_code, quote_currency_code=quote_currency_code) for rate in all_rates
    #     ]

    # async def create_rate(self, as_of: date, base_currency_code: str, quote_currency_code: str, rate: Decimal) -> list[ExchangeRate]:
    #     if base_currency_code == quote_currency_code:
    #         return []

    #     forward_rate = {
    #         "base_currency": base_currency_code,
    #         "target_currency": quote_currency_code,
    #         "rate": float(rate),
    #         "date": as_of.isoformat(),
    #     }
    #     _inverse_rate = 1 / rate
    #     inverse_rate = {
    #         "base_currency": quote_currency_code,
    #         "target_currency": base_currency_code,
    #         "rate": float(_inverse_rate),
    #         "date": as_of.isoformat(),
    #     }

    #     query = self.exchange_house.table(self.table).insert([forward_rate, inverse_rate])

    #     try:
    #         response = query.execute()
    #     except Exception as e:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail=f"Failed to create exchange rate for {base_currency_code} to {quote_currency_code} on {as_of} with error {e}",
    #         ) from e

    #     return [self._parse_response(rate, rate["base_currency"], rate["target_currency"]) for rate in response.data]

    # def _parse_response(self, data: ExchangeRateResponse, base_currency_code: str, quote_currency_code: str) -> ExchangeRate:
    #     return ExchangeRate.from_exchange_house_api(data, base_currency_code, quote_currency_code)
