from fastapi import APIRouter

from app.api.available_dates import router as available_dates_router
from app.api.currency_pairs import router as currency_pair_router
from app.api.historical_exchange_rates import router as historical_exchange_rates_router
from app.api.latest_exchange_rate import router as latest_exchange_rate_router

router = APIRouter(prefix="/exchange_rates")

router.include_router(available_dates_router)
router.include_router(currency_pair_router)
router.include_router(latest_exchange_rate_router)
router.include_router(historical_exchange_rates_router)
