import asyncio
import sys

from tortoise import Tortoise

from app.core.database import TORTOISE_ORM


async def check_db_connection():
    max_retries = 30
    retry_interval = 2  # seconds

    for attempt in range(max_retries):
        try:
            # Try to connect to the database
            await Tortoise.init(TORTOISE_ORM)

            # If connection successful, disconnect and return
            await Tortoise.close_connections()
            print("Database is available and ready.")
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Database not ready yet... ({str(e)})")
            await asyncio.sleep(retry_interval)

    print("Failed to connect to the database after maximum retries")
    return False


if __name__ == "__main__":
    success = asyncio.run(check_db_connection())
    if not success:
        sys.exit(1)  # Exit with error code if DB connection failed
    sys.exit(0)  # Exit successfully if DB connection succeeded
