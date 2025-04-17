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


async def _exchange_rate_refresh() -> str | None:
    async def _update_exchange_rates(exchange_rate_service: ExchangeRateServiceInterface) -> None:
        exchange_rate_refresh = ExchangeRateRefresh(exchange_rate_service=exchange_rate_service)
        await exchange_rate_refresh.save()
        await send_exchange_rate_refresh_email(exchange_rate_service=exchange_rate_service)

    async def _check_in() -> None:
        try:
            healthchecks_client = get_healthchecks_client()
            if settings.refresh_completed_url:
                await healthchecks_client.ping(settings.refresh_completed_url)
            else:
                logger.warning("Skipping healthcheck, as no check-in URL set")
        except Exception as e:
            logger.error(f"Healthcheck failed: {str(e)}")
            return

    await Tortoise.init(config=TORTOISE_ORM)
    try:
        logger.info("Exchange rate refresh task started")
        exchange_rate_service = await get_exchange_rate_service()
        await _update_exchange_rates(exchange_rate_service=exchange_rate_service)
        await _check_in()
        return "Success"
    finally:
        await Tortoise.close_connections()


@celery_app.task(name="app.tasks.exchange_rate_refresh")
def exchange_rate_refresh() -> str | None:
    return asyncio.run(_exchange_rate_refresh())
