import httpx

from app.core.config import settings
from app.core.logger import logger
from app.core.scheduler import metrics


async def heartbeat_task() -> None:
    job_id = "heartbeat"
    metrics.record_job_start(job_id)

    url = settings.heartbeat_check_url
    if not url:
        logger.warning("Heartbeat: check-in failed: URL is not set")
        return

    async with httpx.AsyncClient() as client:
        await client.get(url)

    logger.info("Heartbeat: check-in complete")
