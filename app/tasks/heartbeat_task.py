from app.celery_app import celery_app
from app.core.config import settings
from app.core.logger import logger
from app.services.healthcheck_service import healthcheck_service


@celery_app.task(bind=True, name="app.tasks.heartbeat_task")
def heartbeat_task(self) -> None:  # type: ignore[type-arg]
    if not settings.heartbeat_check_url:
        logger.warning("Heartbeat completed, but no check-in URL set")
        return

    try:
        healthcheck_service.ping_heartbeat()
        logger.info("Heartbeat completed: check-in complete")
    except Exception as e:
        logger.error(f"Heartbeat completed, but check-in failed: {str(e)}")
