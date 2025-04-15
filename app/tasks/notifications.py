from app.core.config import email_settings
from app.core.dependencies import exchange_rate_service_dependency
from app.core.logger import logger
from app.models import Currency
from app.services.email_service import EmailService
from app.services.exchange_rate_service import ExchangeRateServiceInterface


async def send_exchange_rate_refresh_email(
    exchange_rates_service: ExchangeRateServiceInterface = exchange_rate_service_dependency,
) -> None:
    if not email_settings.admin_email:
        logger.warning("No admin email found")
        return

    exchange_rates = await exchange_rates_service.get_historical_rates(
        base_currency_code=Currency("SGD"),
        quote_currency_code=Currency("USD"),
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
      SGDUSD rate for {current_date} = {latest_exchange_rate.rate:.4f}
      ({change:.2%} from {previous_exchange_rate.as_of})
    """

    email_service = EmailService(recipient=email_settings.admin_email, subject=subject, body=body)
    email_service.send()
