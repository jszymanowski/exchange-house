from contextlib import asynccontextmanager

from tortoise import Tortoise

from app.core.config import settings
from app.core.database import TORTOISE_ORM
from app.core.logger import logger
from app.core.scheduler import metrics
from app.integrations.healthchecks import get_healthchecks_client
from app.services.exchange_rate_service import ExchangeRateServiceInterface
from app.tasks.notifications import send_exchange_rate_refresh_email


@asynccontextmanager
async def database_connection():
    await Tortoise.init(TORTOISE_ORM)
    try:
        yield
    finally:
        await Tortoise.close_connections()


async def heartbeat_task() -> None:
    job_id = "heartbeat"
    metrics.record_job_start(job_id)

    if not settings.heartbeat_check_url:
        logger.warning("Heartbeat completed, but check-in failed: URL is not set")
        return

    healthchecks_client = get_healthchecks_client()
    await healthchecks_client.ping(settings.heartbeat_check_url)

    logger.info("Heartbeat completed: check-in complete")


async def latest_exchange_rates_task(exchange_rates_service: ExchangeRateServiceInterface) -> None:
    job_id = "exchange_rate_notification"
    metrics.record_job_start(job_id)

    async with database_connection():
        # exchange_rate_refresh = ExchangeRateRefresh(exchange_rates_service=exchange_rates_service)
        try:
            # await exchange_rate_refresh.save()
            await send_exchange_rate_refresh_email(exchange_rates_service=exchange_rates_service)
        except Exception as e:
            logger.error(f"Exchange rate refresh failed: {str(e)}")
            # TODO: Consider adding metrics.record_job_failure(job_id) if available
            return

    if not settings.refresh_completed_url:
        logger.warning("Refresh completed, but check-in failed: URL is not set")
        return

    healthchecks_client = get_healthchecks_client()
    await healthchecks_client.ping(settings.refresh_completed_url)

    logger.info("Refresh completed: check-in complete")
