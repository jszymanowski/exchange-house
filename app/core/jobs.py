from collections.abc import Callable, Coroutine
from typing import Any, TypeVar

from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from filelock import FileLock, Timeout

from app.core.config import settings
from app.core.dependencies import get_exchange_rate_service
from app.core.logger import logger
from app.core.scheduler import job_listener
from app.tasks.jobs import heartbeat_task, latest_exchange_rates_task

R = TypeVar("R")


def create_task_with_dependencies(func: Callable[..., Coroutine[Any, Any, R]]) -> Callable[..., Coroutine[Any, Any, R]]:
    """Creates a wrapper around a task function that injects required dependencies."""

    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Manually create dependencies
        exchange_rate_service = await get_exchange_rate_service()

        # Call the original function with the dependencies
        return await func(*args, exchange_rate_service=exchange_rate_service, **kwargs)

    return wrapper


class SchedulerManager:
    def __init__(self) -> None:
        self.lock_file = "/tmp/scheduler.lock"
        self.scheduler = AsyncIOScheduler()
        self.lock = FileLock(self.lock_file, timeout=1)
        self._has_lock = False

    def configure_jobs(self) -> None:
        self.scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

        self.scheduler.add_job(
            heartbeat_task, "cron", minute=settings.heartbeat_interval, id="heartbeat", name="Heartbeat check"
        )
        self.scheduler.add_job(
            create_task_with_dependencies(latest_exchange_rates_task),
            "cron",
            hour=settings.exchange_rates_refresh_hour,
            minute=settings.exchange_rates_refresh_minute,
            id="latest_exchange_rates",
            name="Latest exchange rates",
        )

    async def start(self) -> None:
        # Don't start the scheduler outside of production
        if not settings.is_production:
            return

        try:
            acquired = self.lock.acquire(blocking=False)
            if not acquired:
                logger.info("Scheduler already running in another worker")
                return
            self._has_lock = True

            self.configure_jobs()
            if not self.scheduler.running:
                self.scheduler.start()
                logger.info("Scheduler started - this worker owns the scheduler")
        except Timeout:
            logger.info("Scheduler already running in another worker")
        except Exception as e:
            if self._has_lock:
                self.lock.release()
                self._has_lock = False
            logger.error(f"Error starting scheduler: {e}")

    async def shutdown(self) -> None:
        if self.scheduler and self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler shut down")

        if self._has_lock:
            self.lock.release()
            self._has_lock = False


scheduler_manager: SchedulerManager = SchedulerManager()
