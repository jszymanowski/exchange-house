from datetime import date

from fastapi import APIRouter

router = APIRouter()


@router.get("/available_dates")
async def available_dates() -> list[date]:
    return [
        date(2025, 4, 1),
        date(2025, 4, 2),
        date(2025, 4, 3),
    ]
