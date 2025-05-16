from fastapi import APIRouter

from app.api.exchange_rates.available_dates import router as available_dates_router
from app.api.exchange_rates.currency_pairs import router as currency_pair_router
from app.api.exchange_rates.historical_exchange_rates import router as historical_exchange_rates_router
from app.api.exchange_rates.latest_exchange_rate import router as latest_exchange_rate_router

router = APIRouter(prefix="/exchange_rates", tags=["Exchange Rates"])

router.include_router(available_dates_router)
router.include_router(currency_pair_router)
router.include_router(latest_exchange_rate_router)
router.include_router(historical_exchange_rates_router)
