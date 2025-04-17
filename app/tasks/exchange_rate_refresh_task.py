import asyncio

from tortoise import Tortoise

from app.celery_app import celery_app
from app.core.config import settings
from app.core.database import TORTOISE_ORM
from app.core.dependencies import get_exchange_rate_service
from app.core.logger import logger
from app.integrations.healthchecks import get_healthchecks_client
from app.services.exchange_rate_refresh import ExchangeRateRefresh
from app.services.exchange_rate_service import ExchangeRateServiceInterface
from app.tasks.notifications import send_exchange_rate_refresh_email


@celery_app.task(name="app.tasks.exchange_rate_refresh")
def exchange_rate_refresh():
    """Regular synchronous Celery task that manages the async code inside."""

    async def _update_exchange_rates(exchange_rate_service: ExchangeRateServiceInterface):
        exchange_rate_refresh = ExchangeRateRefresh(exchange_rate_service=exchange_rate_service)
        await exchange_rate_refresh.save()
        await send_exchange_rate_refresh_email(exchange_rate_service=exchange_rate_service)

    async def _check_in():
        try:
            healthchecks_client = get_healthchecks_client()
            await healthchecks_client.ping(settings.refresh_completed_url)
        except Exception as e:
            logger.error(f"Healthcheck failed: {str(e)}")
            return

    async def _async_task():
        await Tortoise.init(config=TORTOISE_ORM)
        try:
            exchange_rate_service = await get_exchange_rate_service()
            await _update_exchange_rates(exchange_rate_service=exchange_rate_service)
            await _check_in()
        finally:
            await Tortoise.close_connections()

    # Run the async code from our synchronous task
    result = asyncio.run(_async_task())
    logger.info(f"Exchange rate refresh completed with result: {result}")
    return result
