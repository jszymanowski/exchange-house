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
            from_iso_code="USD",
            to_iso_code="EUR",
        ),
        CurrencyPairResponse(
            from_iso_code="EUR",
            to_iso_code="USD",
        ),
        CurrencyPairResponse(
            from_iso_code="USD",
            to_iso_code="GBP",
        ),
        CurrencyPairResponse(
            from_iso_code="GBP",
            to_iso_code="USD",
        ),
    ]
