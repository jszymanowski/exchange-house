from celery import Celery

from app.core.config import celery_settings

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


# Add custom task base to all tasks
class BaseTask(celery_app.Task):
    """Base task class with error handling and logging."""

    def on_success(self, retval, task_id, args, kwargs):
        """Log success."""
        print(f"Task {task_id} completed successfully with result: {retval}")
        return super().on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Log failure."""
        print(f"Task {task_id} failed: {exc}")
        return super().on_failure(exc, task_id, args, kwargs, einfo)


# Use the custom task class for all tasks by default
celery_app.Task = BaseTask


celery_app.conf.beat_schedule = {
    "heartbeat": {
        "task": "app.tasks.heartbeat_task",
        "schedule": 60.0,  # 1 minute
        "args": ("Heartbeat",),
    },
}
