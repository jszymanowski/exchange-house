from fastapi import APIRouter

from app.core.dependencies import exchange_rate_service_dependency
from app.schema.currency_pair_response import CurrencyPairResponse
from app.services.exchange_rate_service import ExchangeRateServiceInterface

router = APIRouter()


@router.get(
    "/available_currency_pairs",
    summary="Get available currency pairs",
    description="Returns a list of all supported currency pairs for exchange rate conversions.",
)
async def currency_pairs(
    exchange_rate_service: ExchangeRateServiceInterface = exchange_rate_service_dependency,
) -> list[CurrencyPairResponse]:
    currency_pairs = await exchange_rate_service.get_currency_pairs()
    return [
        CurrencyPairResponse(
            base_currency_code=pair.base_currency_code,
            quote_currency_code=pair.quote_currency_code,
        )
        for pair in currency_pairs
    ]
