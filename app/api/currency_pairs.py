from fastapi import APIRouter

from app.schema.currency_pair_response import CurrencyPairResponse

router = APIRouter()


@router.get(
    "/currency_pairs",
    summary="Get available currency pairs",
    description="Returns a list of all supported currency pairs for exchange rate conversions.",
)
async def currency_pairs() -> list[CurrencyPairResponse]:
    return [
        CurrencyPairResponse(
            base_currency_code="USD",
            quote_currency_code="EUR",
        ),
        CurrencyPairResponse(
            base_currency_code="EUR",
            quote_currency_code="USD",
        ),
        CurrencyPairResponse(
            base_currency_code="USD",
            quote_currency_code="GBP",
        ),
        CurrencyPairResponse(
            base_currency_code="GBP",
            quote_currency_code="USD",
        ),
    ]
