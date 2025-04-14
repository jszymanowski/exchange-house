import os

from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from filelock import FileLock, Timeout

from app.core.logger import logger
from app.core.scheduler import job_listener
from app.tasks.jobs import heartbeat_task


class SchedulerManager:
    def __init__(self) -> None:
        self.lock_file = "/tmp/scheduler.lock"
        self.scheduler = AsyncIOScheduler()
        self.lock = FileLock(self.lock_file, timeout=1)
        self._has_lock = False

    def configure_jobs(self) -> None:
        self.scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

        self.scheduler.add_job(heartbeat_task, "cron", minute="*/5", id="heartbeat", name="Heartbeat check")

    async def start(self) -> None:
        # Don't start the scheduler outside of production
        if os.environ.get("ENV") != "production":
            return

        try:
            self.lock.acquire(blocking=False)
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
