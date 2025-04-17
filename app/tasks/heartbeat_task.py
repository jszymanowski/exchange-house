from app.celery_app import celery_app
from app.core.config import settings
from app.core.logger import logger
from app.services.healthcheck_service import healthcheck_service
from app.tasks.task_result import TaskResult, failure_result, skipped_result, success_result


@celery_app.task(name="app.tasks.heartbeat_task")
def heartbeat_task() -> TaskResult:
    if not settings.heartbeat_check_url:
        logger.warning("Heartbeat completed, but no check-in URL set")
        return skipped_result("Heartbeat completed, but no check-in URL set")

    try:
        healthcheck_service.ping_heartbeat()  # TODO: make this async
        logger.info("Heartbeat completed: check-in complete")
        return success_result()
    except Exception as e:
        logger.error(f"Heartbeat completed, but check-in failed: {str(e)}")
        return failure_result(f"Heartbeat completed, but check-in failed: {str(e)}")
