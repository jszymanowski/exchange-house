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

    async def get_latest_rate(self, from_iso_code: str, to_iso_code: str, as_of: date) -> ExchangeRate | None:
        raise RuntimeError("Must be implemented")

    async def get_historical_rates(
        self,
        from_iso_code: str,
        to_iso_code: str,
        start_date: date | None = None,
        limit: int | None = None,
        sort_order: Literal["asc", "desc"] = "asc",
    ) -> list[ExchangeRate]:
        raise RuntimeError("Must be implemented")

    async def create_rate(self, as_of: date, from_iso_code: str, to_iso_code: str, rate: Decimal) -> list[ExchangeRate]:
        raise RuntimeError("Must be implemented")


# class LegacyExchangeRateService(ExchangeRateServiceInterface):
#     def __init__(self, db_session: AsyncSession):
#         self.db_session = db_session

#     async def get_currency_pairs(self) -> list[CurrencyPair]:
#         query = select(LegacyExchangeRate).distinct(LegacyExchangeRate.from_iso_code, LegacyExchangeRate.to_iso_code)
#         result = await self.db_session.execute(query)
#         exchange_rates = result.scalars().all()
#         logging.info(f"exchange_rates: {exchange_rates}")

#         return [CurrencyPair.from_db(exchange_rate) for exchange_rate in exchange_rates]

#     async def get_available_dates(self) -> list[date]:
#         stmt = select(LegacyExchangeRate.as_of).distinct()
#         result = await self.db_session.execute(stmt)
#         return [row[0] for row in result.fetchall()]

#     async def get_latest_rate(self, from_iso_code: str, to_iso_code: str, as_of: date) -> Optional[ExchangeRate]:
#         if from_iso_code == to_iso_code:
#             return ExchangeRate(
#                 rate=Decimal(1),
#                 date=as_of,
#                 from_iso_code=from_iso_code,
#                 to_iso_code=to_iso_code,
#             )

#         query = (
#             select(LegacyExchangeRate)
#             .where(
#                 and_(
#                     LegacyExchangeRate.from_iso_code == from_iso_code,
#                     LegacyExchangeRate.to_iso_code == to_iso_code,
#                     LegacyExchangeRate.as_of <= as_of,
#                 )
#             )
#             .order_by(LegacyExchangeRate.as_of.desc())
#             .limit(1)
#         )

#         result = await self.db_session.execute(query)
#         exchange_rate = result.scalar_one_or_none()

#         if exchange_rate:
#             return ExchangeRate(
#                 rate=exchange_rate.rate,
#                 date=exchange_rate.as_of,
#                 from_iso_code=CurrencyCode(exchange_rate.from_iso_code),
#                 to_iso_code=CurrencyCode(exchange_rate.to_iso_code),
#             )

#         return None

#     async def get_historical_rates(
#         self,
#         from_iso_code: str,
#         to_iso_code: str,
#         start_date: Optional[date] = None,
#         limit: Optional[int] = None,
#         sort_order: Literal["asc", "desc"] = "asc",
#     ) -> list[ExchangeRate]:
#         query = select(LegacyExchangeRate).where(
#             LegacyExchangeRate.from_iso_code == from_iso_code,
#             LegacyExchangeRate.to_iso_code == to_iso_code,
#         )
#         if sort_order == "desc":
#             query = query.order_by(LegacyExchangeRate.as_of.desc())
#         else:
#             query = query.order_by(LegacyExchangeRate.as_of.asc())

#         if start_date is not None:
#             query = query.where(LegacyExchangeRate.as_of >= start_date)
#         if limit is not None:
#             query = query.limit(limit)
#         result = await self.db_session.execute(query)
#         exchange_rates = result.scalars().all()

#         return [ExchangeRate.from_db(exchange_rate) for exchange_rate in exchange_rates]

#     async def create_rate(self, as_of: date, from_iso_code: str, to_iso_code: str, rate: Decimal) -> list[ExchangeRate]:
#         if from_iso_code == to_iso_code:
#             return []

#         forward_rate = LegacyExchangeRate(as_of=as_of, from_iso_code=from_iso_code, to_iso_code=to_iso_code, rate=rate)
#         _inverse_rate = 1 / rate
#         inverse_rate = LegacyExchangeRate(
#             as_of=as_of, from_iso_code=to_iso_code, to_iso_code=from_iso_code, rate=_inverse_rate
#         )
#         self.db_session.add_all([forward_rate, inverse_rate])

#         await self.db_session.commit()

#         return [ExchangeRate.from_db(forward_rate), ExchangeRate.from_db(inverse_rate)]


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

    # async def get_latest_rate(self, from_iso_code: str, to_iso_code: str, as_of: date) -> ExchangeRate | None:
    #     if from_iso_code == to_iso_code:
    #         return ExchangeRate(
    #             rate=Decimal(1),
    #             date=as_of,
    #             from_iso_code=from_iso_code,
    #             to_iso_code=to_iso_code,
    #         )

    #     if (from_iso_code == "CUSTOM_AMEX" and to_iso_code == "USD") or (
    #         from_iso_code == "USD" and to_iso_code == "CUSTOM_AMEX"
    #     ):
    #         return get_custom_currency_rate(from_iso_code, to_iso_code, as_of)

    #     if (from_iso_code == "CUSTOM_CAPITAL_ONE" and to_iso_code == "USD") or (
    #         from_iso_code == "USD" and to_iso_code == "CUSTOM_CAPITAL_ONE"
    #     ):
    #         return get_custom_currency_rate(from_iso_code, to_iso_code, as_of)

    #     query = (
    #         self.exchange_house.table(self.table)
    #         .select("rate, date")
    #         .eq("base_currency", from_iso_code)
    #         .eq("target_currency", to_iso_code)
    #         .order("date", desc=True)
    #         .limit(1)
    #     )

    #     response = query.execute()

    #     if not response.data:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f"No exchange rates found for {from_iso_code} to {to_iso_code}",
    #         )

    #     return self._parse_response(response.data[0], from_iso_code, to_iso_code)

    # async def get_historical_rates(
    #     self,
    #     from_iso_code: str,
    #     to_iso_code: str,
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
    #         .eq("base_currency", from_iso_code)
    #         .eq("target_currency", to_iso_code)
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
    #             detail=f"No exchange rates found for {from_iso_code}"
    #             f" to {to_iso_code} between {start_date} and {end_date}",
    #         )

    #     if len(all_rates) == MAX_RECORDS_PER_REQUEST:
    #         logger.warning(f"Reached the maximum number of records per request: {MAX_RECORDS_PER_REQUEST}")

    #     return [
    #         self._parse_response(data=rate, from_iso_code=from_iso_code, to_iso_code=to_iso_code) for rate in all_rates
    #     ]

    # async def create_rate(self, as_of: date, from_iso_code: str, to_iso_code: str, rate: Decimal) -> list[ExchangeRate]:
    #     if from_iso_code == to_iso_code:
    #         return []

    #     forward_rate = {
    #         "base_currency": from_iso_code,
    #         "target_currency": to_iso_code,
    #         "rate": float(rate),
    #         "date": as_of.isoformat(),
    #     }
    #     _inverse_rate = 1 / rate
    #     inverse_rate = {
    #         "base_currency": to_iso_code,
    #         "target_currency": from_iso_code,
    #         "rate": float(_inverse_rate),
    #         "date": as_of.isoformat(),
    #     }

    #     query = self.exchange_house.table(self.table).insert([forward_rate, inverse_rate])

    #     try:
    #         response = query.execute()
    #     except Exception as e:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail=f"Failed to create exchange rate for {from_iso_code} to {to_iso_code} on {as_of} with error {e}",
    #         ) from e

    #     return [self._parse_response(rate, rate["base_currency"], rate["target_currency"]) for rate in response.data]

    # def _parse_response(self, data: ExchangeRateResponse, from_iso_code: str, to_iso_code: str) -> ExchangeRate:
    #     return ExchangeRate.from_exchange_house_api(data, from_iso_code, to_iso_code)
