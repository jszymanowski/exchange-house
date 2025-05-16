from fastapi import Depends

from app.services.exchange_rate_service import (
    ExchangeRateService,
    ExchangeRateServiceInterface,
)
from app.services.firebase_service import FirebaseService


async def get_exchange_rate_service() -> ExchangeRateServiceInterface:
    return ExchangeRateService()


exchange_rate_service_dependency = Depends(get_exchange_rate_service)


async def get_firebase_service() -> FirebaseService:
    return FirebaseService()


firebase_service_dependency = Depends(get_firebase_service)
