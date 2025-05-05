import asyncio

from app.celery_app import celery_app
from app.core.logger import get_logger
from app.services.healthchecks_service import NoURLSetError, get_healthchecks_service
from app.tasks.task_result import TaskResult, failure_result, skipped_result, success_result


async def _heartbeat_task() -> TaskResult:
    logger = get_logger("heartbeat")

    try:
        await get_healthchecks_service.ping_heartbeat()
        logger.info("Heartbeat completed: check-in complete")
        return success_result()
    except NoURLSetError:
        logger.warning("Heartbeat completed, but no check-in URL set")
        return skipped_result("Heartbeat completed, but no check-in URL set")
    except Exception as e:
        logger.error(f"Heartbeat completed, but check-in failed: {str(e)}")
        return failure_result(f"Heartbeat completed, but check-in failed: {str(e)}")


@celery_app.task(name="app.tasks.heartbeat_task")
def heartbeat_task() -> TaskResult:
    return asyncio.run(_heartbeat_task())
