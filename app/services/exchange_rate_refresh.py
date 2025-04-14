from datetime import date, datetime, timedelta
from decimal import Decimal

from app.integrations.open_exchange_rates import OpenExchangeRatesClient
from app.services.exchange_rate_service import ExchangeRateServiceInterface


class ExchangeRateRefresh:
    SAMPLE_CURRENCY = "EUR"
    BASE_CURRENCY = "USD"
    DATA_SOURCE = "openexchangerates.org"

    def __init__(
        self,
        exchange_rate_service: ExchangeRateServiceInterface,
        start_date: date | None = None,
        end_date: date | None = None,
    ):
        self.start_date = start_date or (datetime.now().date() - timedelta(days=8))
        self.end_date = end_date or (datetime.now().date() - timedelta(days=1))
        self.api_client = OpenExchangeRatesClient()
        self.exchange_rates_service = exchange_rate_service

    async def save(self) -> None:
        dates = await self._get_all_dates()

        for target_date in dates:
            try:
                data = await self.api_client.historical_rates_for(target_date)
                for to_currency, rate in data.rates.items():
                    await self.exchange_rates_service.create_rate(
                        as_of=target_date,
                        base_currency_code=self.BASE_CURRENCY,
                        quote_currency_code=to_currency,
                        rate=Decimal(rate),
                        source=self.DATA_SOURCE,
                    )

            except Exception as e:
                print(f"Error processing {target_date}: {str(e)}")
                raise

    async def _get_all_dates(self) -> list[date]:
        frequency_dates = [
            self.start_date + timedelta(days=x) for x in range((self.end_date - self.start_date).days + 1)
        ]
        existing_dates = await self.exchange_rates_service.get_available_dates()

        all_dates = set([self.start_date, self.end_date] + frequency_dates)
        return sorted(all_dates - set(existing_dates))
