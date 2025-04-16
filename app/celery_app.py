from typing import Any

from celery import Celery
from celery.app.task import Task
from celery.schedules import crontab

from app.core.config import celery_settings
from app.core.logger import logger

# Monkey patch Task class to avoid type errors, as recommended in celery-type docs: https://pypi.org/project/celery-types/
Task.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)  # type: ignore[attr-defined]


celery_app = Celery(
    "worker",
    broker=celery_settings.celery_broker_url,
    backend=celery_settings.celery_backend_url,
    include=["app.tasks"],
)

celery_app.conf.update(
    task_track_started=True,  # Task will report 'started' state when started
    task_time_limit=10 * 60,  # 10 minutes time limit
    task_soft_time_limit=5 * 60,  # 5 minutes soft time limit
    worker_prefetch_multiplier=1,  # Don't prefetch more tasks than workers can handle
    task_send_sent_event=True,  # Required for monitoring task queue length in Flower
    result_expires=60 * 60 * 24,  # Results expire after 24 hours
)


class BaseTask(Task):  # type: ignore[type-arg]
    """Base task class with error handling and logging."""

    def on_success(self, retval: Any, task_id: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> None:
        """Log success."""
        logger.info(f"Task {task_id} completed successfully with result: {retval}")
        return super().on_success(retval, task_id, args, kwargs)

    def on_failure(
        self, exc: Exception, task_id: str, args: tuple[Any, ...], kwargs: dict[str, Any], einfo: Any
    ) -> None:
        """Log failure."""
        logger.error(f"Task {task_id} failed: {exc}")
        return super().on_failure(exc, task_id, args, kwargs, einfo)


# Use the custom task class for all tasks by default
celery_app.conf.task_cls = "BaseTask"


celery_app.conf.beat_schedule = {
    "heartbeat": {
        "task": "heartbeat_task",
        "schedule": crontab(minute=celery_settings.heartbeat_interval),
        "args": ("Heartbeat",),
    },
}
