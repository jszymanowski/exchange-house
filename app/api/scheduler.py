from typing import TypedDict

from fastapi import APIRouter

from app.core.scheduler import JobStats, metrics, scheduler

router = APIRouter()


class JobSummary(TypedDict, total=False):
    id: str
    name: str
    next_run_time: str | None
    pending: bool


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
    return metrics.job_stats
