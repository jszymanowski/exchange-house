from datetime import date, datetime, timedelta
from decimal import Decimal

from app.core.logger import logger
from app.integrations.open_exchange_rates import HistoricalRatesResponse, OpenExchangeRatesClient
from app.models import Currency
from app.services.exchange_rate_service import CreateRateParams, ExchangeRateServiceInterface


class ExchangeRateRefresh:
    """Service to refresh exchange rates from Open Exchange Rates API.

    Fetches historical exchange rates for a date range and stores them using
    the provided exchange rate service.
    """

    SAMPLE_CURRENCY = Currency("EUR")
    BASE_CURRENCY = Currency("USD")
    DATA_SOURCE = "openexchangerates.org"

    def __init__(
        self,
        exchange_rate_service: ExchangeRateServiceInterface,
        start_date: date | None = None,
        end_date: date | None = None,
    ):
        """Initialize the exchange rate refresh service.

        Args:
            exchange_rate_service: Service to store exchange rates
            start_date: Start date for rate retrieval (default: 8 days ago)
            end_date: End date for rate retrieval (default: yesterday)
        """
        self.start_date = start_date or (datetime.now().date() - timedelta(days=8))
        self.end_date = end_date or (datetime.now().date() - timedelta(days=1))
        self.api_client = OpenExchangeRatesClient()
        self.exchange_rates_service = exchange_rate_service

    async def save(self) -> None:
        """Fetch and save exchange rates for all required dates.

        Retrieves historical exchange rates for each date in the date range
        that doesn't already have rates stored. Saves each currency pair rate.

        Raises:
            Exception: If there's an error retrieving or saving the rates.
        """
        dates = await self._get_all_dates()

        for target_date in dates:
            try:
                data = await self.api_client.historical_rates_for(target_date)
                await self._save_rates(target_date, data)

            except Exception as e:
                logger.error(f"Error processing rates for date {target_date}: {str(e)}", exc_info=True)
                raise

    async def _save_rates(self, target_date: date, data: HistoricalRatesResponse) -> None:
        params = [
            CreateRateParams(
                as_of=target_date,
                base_currency_code=self.BASE_CURRENCY,
                quote_currency_code=Currency(to_currency),
                rate=Decimal(rate),
                source=self.DATA_SOURCE,
            )
            for to_currency, rate in data.rates.items()
        ]
        await self.exchange_rates_service.bulk_create_rates(params)

    async def _get_all_dates(self) -> list[date]:
        """Get a list of dates that need exchange rates to be fetched.

        Returns only dates in the specified range that don't already have
        exchange rates stored.

        Returns:
            A sorted list of dates requiring exchange rate data.
        """
        frequency_dates = [
            self.start_date + timedelta(days=x) for x in range((self.end_date - self.start_date).days + 1)
        ]
        existing_dates = await self.exchange_rates_service.get_available_dates()
        # start_date and end_date are already included in frequency_dates
        all_dates = set(frequency_dates)
        return sorted(all_dates - set(existing_dates))
