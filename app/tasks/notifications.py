from app.core.config import email_settings
from app.core.dependencies import exchange_rate_service_dependency
from app.core.logger import logger
from app.models import Currency
from app.services.email_service import EmailService
from app.services.exchange_rate_service import ExchangeRateServiceInterface

DEFAULT_BASE_CURRENCY = Currency("SGD")
DEFAULT_QUOTE_CURRENCY = Currency("USD")


async def send_exchange_rate_refresh_email(
    exchange_rates_service: ExchangeRateServiceInterface = exchange_rate_service_dependency,
    base_currency: Currency = DEFAULT_BASE_CURRENCY,
    quote_currency: Currency = DEFAULT_QUOTE_CURRENCY,
) -> None:
    if not email_settings.admin_email:
        logger.warning("No admin email found")
        return

    exchange_rates = await exchange_rates_service.get_historical_rates(
        base_currency_code=base_currency,
        quote_currency_code=quote_currency,
        limit=2,
        sort_order="desc",
    )

    if len(exchange_rates) < 2:
        logger.warning("Not enough exchange rates found")
        return

    latest_exchange_rate, previous_exchange_rate = exchange_rates
    current_date = latest_exchange_rate.as_of
    change = (latest_exchange_rate.rate - previous_exchange_rate.rate) / previous_exchange_rate.rate

    subject = f"[ExchangeHouse] Exchange rates for {current_date}"
    body = f"""
      {base_currency}{quote_currency} rate for {current_date} = {latest_exchange_rate.rate:.4f}
      ({change:.2%} from {previous_exchange_rate.as_of})
    """

    email_service = EmailService(recipient=email_settings.admin_email, subject=subject, body=body)
    email_service.send_async()
