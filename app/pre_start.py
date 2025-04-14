import asyncio
import sys

from aerich import Command
from tortoise import Tortoise

from app.core.database import TORTOISE_ORM
from app.core.logger import logger


async def check_db_connection() -> bool:
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
        except ConnectionRefusedError as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Database connection refused ({str(e)})")
            await asyncio.sleep(retry_interval)
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Database not ready yet - unexpected error ({str(e)})")
            await asyncio.sleep(retry_interval)

    print("Failed to connect to the database after maximum retries")
    return False


async def init_db() -> bool:
    try:
        async with Command(tortoise_config=TORTOISE_ORM) as command:
            await command.upgrade()
            return True
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return False


def main() -> None:
    success = asyncio.run(check_db_connection())
    if not success:
        logger.error("Failed to connect to database, exiting")
        sys.exit(1)
    logger.info("Database connection successful")

    success = asyncio.run(init_db())
    if not success:
        logger.error("Failed to initialize database, exiting")
        sys.exit(0)  # TODO: change to 1
    logger.info("Database initialized successfully")

    sys.exit(0)


if __name__ == "__main__":
    main()
