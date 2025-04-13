from datetime import date

from fastapi import APIRouter

router = APIRouter()


@router.get("/available_dates")
async def available_dates() -> list[date]:
    """
    Retrieve a list of available dates for exchange rate data.

    Returns:
        list[date]: List of dates for which exchange rate data is available
    """
    return [
        date(2025, 4, 1),
        date(2025, 4, 2),
        date(2025, 4, 3),
    ]
