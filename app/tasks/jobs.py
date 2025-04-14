from app.core.config import settings
from app.core.dependencies import get_exchange_rate_service
from app.core.logger import logger
from app.core.scheduler import metrics
from app.integrations.healthchecks import get_healthchecks_client
from app.services.exchange_rate_refresh import ExchangeRateRefresh


async def heartbeat_task() -> None:
    job_id = "heartbeat"
    metrics.record_job_start(job_id)

    if not settings.heartbeat_check_url:
        logger.warning("Heartbeat completed, but check-in failed: URL is not set")
        return

    healthchecks_client = get_healthchecks_client()
    await healthchecks_client.ping(settings.heartbeat_check_url)

    logger.info("Heartbeat completed: check-in complete")


async def latest_exchange_rates_task() -> None:
    job_id = "exchange_rate_notification"
    metrics.record_job_start(job_id)

    exchange_rates_service = await get_exchange_rate_service()
    exchange_rate_refresh = ExchangeRateRefresh(exchange_rate_service=exchange_rates_service)
    try:
        await exchange_rate_refresh.save()
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
