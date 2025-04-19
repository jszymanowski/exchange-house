from app.celery_app import celery_app
from app.core.logger import logger
from app.services.healthchecks_service import NoURLSetError, healthchecks_service
from app.tasks.task_result import TaskResult, failure_result, skipped_result, success_result


@celery_app.task(name="app.tasks.heartbeat_task")
def heartbeat_task() -> TaskResult:
    try:
        healthchecks_service.ping_heartbeat()  # TODO: make this async
        logger.info("Heartbeat completed: check-in complete")
        return success_result()
    except NoURLSetError:
        logger.warning("Heartbeat completed, but no check-in URL set")
        return skipped_result("Heartbeat completed, but no check-in URL set")
    except Exception as e:
        logger.error(f"Heartbeat completed, but check-in failed: {str(e)}")
        return failure_result(f"Heartbeat completed, but check-in failed: {str(e)}")
