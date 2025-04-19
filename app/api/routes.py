from fastapi import APIRouter

from app.api.exchange_rates.routes import router as exchange_rates_router

router = APIRouter(prefix="/api/v1")

router.include_router(exchange_rates_router)
