import argparse
import asyncio
import sys

from tortoise import Tortoise

from app.core.database import TORTOISE_ORM
from app.core.dependencies import get_exchange_rate_service, get_firebase_service
from app.models import Currency, ExchangeRate


async def upload_currencies() -> tuple[bool, Exception | None]:
    """Upload currencies to Firebase and return success status."""

    try:
        firebase_service = await get_firebase_service()
        result = firebase_service.update_currencies()
        return result
    except Exception as e:
        print(f"Uploading currencies failed: {e}", file=sys.stderr)
        return False, e


async def _get_latest_exchange_rates() -> list[ExchangeRate]:
    exchange_rate_service = await get_exchange_rate_service()

    try:
        await Tortoise.init(config=TORTOISE_ORM)
        rates = await exchange_rate_service.get_latest_rates(
            base_currency_code=Currency("USD"),
        )

        return rates
    except Exception as e:
        print(f"Retrieving latest exchange rates failed: {e}", file=sys.stderr)
        return []
    finally:
        await Tortoise.close_connections()


async def upload_exchange_rates(exchange_rates: list[ExchangeRate]) -> tuple[bool, Exception | None]:
    """Upload exchange rates to Firebase and return success status."""

    try:
        firebase_service = await get_firebase_service()
        result = firebase_service.update_exchange_rates(exchange_rates)
        return result
    except Exception as e:
        print(f"Uploading exchange rates failed: {e}", file=sys.stderr)
        return False, e


if __name__ == "__main__":
    """
    Manually upload exchange rates to Firebase.

    Example:
        uv run python -m cli.firebase
    """
    parser = argparse.ArgumentParser(description="Manually upload exchange rates to Firebase")
    args = parser.parse_args()

    exchange_rates = asyncio.run(_get_latest_exchange_rates())

    if len(exchange_rates) == 0:
        print("No exchange rates found", file=sys.stderr)
        sys.exit(1)

    print("Uploading currencies...")
    currencies_result = asyncio.run(upload_currencies())
    if currencies_result[0]:
        print("success")
    else:
        print(f"failed: {currencies_result[1]}", file=sys.stderr)
        sys.exit(1)

    print("Uploading exchange rates...")
    exchange_rates_result = asyncio.run(upload_exchange_rates(exchange_rates))
    if exchange_rates_result[0]:
        print("success")
    else:
        print(f"failed: {exchange_rates_result[1]}", file=sys.stderr)
        sys.exit(1)

    print("\nCurrencies and exchange rates uploaded successfully")
    sys.exit(0)
