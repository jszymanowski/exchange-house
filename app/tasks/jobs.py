from app.core.logger import logger
from app.core.scheduler import metrics


async def heartbeat_task() -> None:
    job_id = "heartbeat"
    metrics.record_job_start(job_id)
    logger.info("Heartbeat check complete")
