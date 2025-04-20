from fastapi import APIRouter

from app.core.dependencies import exchange_rate_service_dependency
from app.schema.date_list_response import DateListResponse
from app.services.exchange_rate_service import ExchangeRateServiceInterface

router = APIRouter()


@router.get("/available_dates")
async def available_dates(
    exchange_rate_service: ExchangeRateServiceInterface = exchange_rate_service_dependency,
) -> DateListResponse:
    """
    Retrieve a list of available dates for exchange rate data.

    """
    Retrieve a list of available dates for exchange rate data.

    Returns:
        DateListResponse: Object containing a list of dates for which exchange rate data is available
    """
    dates = await exchange_rate_service.get_available_dates()
    return DateListResponse(data=dates)
