import argparse
import asyncio
import sys

from tortoise import Tortoise

from app.core.database import TORTOISE_ORM
from app.core.dependencies import get_exchange_rate_service, get_firebase_service
from app.models import Currency, ExchangeRate


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
        return False
    finally:
        await Tortoise.close_connections()


async def upload_exchange_rates(exchange_rates: list[ExchangeRate]) -> bool:
    """Run the exchange rate refresh process for the specified date range."""

    try:
        firebase_service = await get_firebase_service()
        firebase_service.update_exchange_rates(exchange_rates)
        return True
    except Exception as e:
        print(f"Uploading exchange rates failed: {e}", file=sys.stderr)
        raise e
        # return False


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

    result = asyncio.run(upload_exchange_rates(exchange_rates))
    sys.exit(0 if result else 1)
