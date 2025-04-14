from typing import TypedDict

from fastapi import APIRouter

from app.core.scheduler import JobStats, metrics, scheduler

router = APIRouter()


class JobSummary(TypedDict, total=False):
    """Summary information for a scheduled job."""

    id: str
    """Unique identifier for the job."""
    name: str
    """Human-readable name of the job."""
    next_run_time: str | None
    """ISO-formatted timestamp of the next scheduled run, or None if not scheduled."""
    pending: bool
    """Whether the job is currently pending execution."""


@router.get("/jobs")
async def get_jobs() -> list[JobSummary]:
    jobs = scheduler.get_jobs()
    return [
        JobSummary(
            id=job.id,
            name=job.name,
            next_run_time=job.next_run_time.isoformat() if job.next_run_time else None,
            pending=job.pending,
        )
        for job in jobs
    ]


@router.get("/metrics")
async def get_metrics() -> dict[str, JobStats]:
    """Return statistics for all scheduled jobs, including run counts and execution times."""
    return metrics.job_stats
