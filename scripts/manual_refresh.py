import argparse
import asyncio
from datetime import date, datetime

from app.core.dependencies import get_exchange_rate_service
from app.services.exchange_rate_refresh import build_exchange_rate_refresh


def run_manual_refresh(start_date: date, end_date: date) -> bool:
    exchange_rate_service = asyncio.run(get_exchange_rate_service())
    exchange_rate_refresh = build_exchange_rate_refresh(
        exchange_rate_service=exchange_rate_service,
        start_date=start_date,
        end_date=end_date,
    )
    result = asyncio.run(exchange_rate_refresh.save())

    if not result:
        print("Refresh failed; check logs for more information")
        return False

    print("Refresh completed successfully")
    return True


if __name__ == "__main__":
    """
    Manually refresh exchange rates for a date range.

    Example:
        python -m scripts.manual_refresh --start-date 2025-01-01 --end-date 2025-01-31
    """
    parser = argparse.ArgumentParser(description="Manually refresh exchange rates for a date range")
    parser.add_argument("--start-date", type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end-date", type=str, help="End date in YYYY-MM-DD format")

    args = parser.parse_args()

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d").date() if args.start_date else None
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d").date() if args.end_date else None

    result = run_manual_refresh(start_date=start_date, end_date=end_date)
    print(f"Refresh completed with result: {result}")
