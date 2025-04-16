from datetime import datetime
from typing import TypedDict

from apscheduler.events import JobExecutionEvent
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import settings
from app.core.logger import logger


class JobStats(TypedDict, total=False):
    start_time: datetime
    end_time: datetime
    duration: float
    success: bool
    runs: int
    failures: int


class JobMetrics:
    def __init__(self) -> None:
        self.job_stats: dict[str, JobStats] = {}

    def record_job_start(self, job_id: str) -> None:
        if job_id not in self.job_stats:
            self.job_stats[job_id] = {}
        self.job_stats[job_id]["start_time"] = datetime.now()

    def record_job_end(self, job_id: str, success: bool) -> None:
        if job_id in self.job_stats:
            stats = self.job_stats[job_id]
            stats["end_time"] = datetime.now()
            stats["duration"] = (stats["end_time"] - stats["start_time"]).total_seconds()
            stats["success"] = success
            stats["runs"] = stats.get("runs", 0) + 1
            if not success:
                stats["failures"] = stats.get("failures", 0) + 1
            else:
                stats["failures"] = stats.get("failures", 0)

    def record_job_failure(self, job_id: str) -> None:
        if job_id in self.job_stats:
            stats = self.job_stats[job_id]
            stats["failures"] = stats.get("failures", 0) + 1


scheduler = AsyncIOScheduler(timezone=settings.timezone, job_defaults={"coalesce": True, "max_instances": 1})
metrics = JobMetrics()


def job_listener(event: JobExecutionEvent) -> None:
    if event.exception:
        logger.error(f"Job {event.job_id} failed: {event.exception}")
        metrics.record_job_end(event.job_id, False)
    else:
        logger.info(f"Job {event.job_id} completed successfully")
        metrics.record_job_end(event.job_id, True)
