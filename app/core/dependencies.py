from fastapi import Depends

from app.services.exchange_rate_service import (
    ExchangeRateService,
    ExchangeRateServiceInterface,
)


async def get_exchange_rate_service() -> ExchangeRateServiceInterface:
    return ExchangeRateService()


exchange_rate_service_dependency = Depends(get_exchange_rate_service)
