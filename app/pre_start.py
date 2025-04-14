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
            logger.info(f"Attempt {attempt + 1}/{max_retries}: Connecting to database...")
            await Tortoise.init(TORTOISE_ORM)

            # If connection successful, try to run a simple query to ensure full readiness
            conn = Tortoise.get_connection("default")
            await conn.execute_query("SELECT 1")

            # If we get here, connection is fully established
            await Tortoise.close_connections()
            logger.info("Database is available and ready.")
            return True

        except Exception as e:
            logger.warning(
                f"Attempt {attempt + 1}/{max_retries}: Database not ready yet - {e.__class__.__name__}: {str(e)}"
            )
            # Close any partial connections before retrying
            try:
                await Tortoise.close_connections()
            except Exception as e:
                pass
            await asyncio.sleep(retry_interval)

    logger.error("Failed to connect to the database after maximum retries")
    return False


async def init_db() -> bool:
    try:
        async with Command(tortoise_config=TORTOISE_ORM, location="migrations") as command:
            await command.upgrade()
            return True
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return False


def main() -> None:
    logger.info("Starting database connection check...")
    success = asyncio.run(check_db_connection())
    if not success:
        logger.error("Failed to initialize database, exiting")
        sys.exit(1)
    logger.info("Database connection successful")

    success = asyncio.run(init_db())
    if not success:
        logger.error("Failed to initialize database, exiting")
        sys.exit(1)
    logger.info("Database initialized successfully")

    sys.exit(0)


if __name__ == "__main__":
    main()
