import os
from functools import cached_property

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Exchange House"
    PROJECT_DESCRIPTION: str = "A simple API for exchange rates"
    PROJECT_VERSION: str = "v1"

    @property
    def environment(self) -> str:
        return os.getenv("ENV", "development")

    @property
    def is_test(self) -> bool:
        return self.environment == "test"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def timezone(self) -> str:
        return os.getenv("TIMEZONE", "UTC")

    @property
    def logging_level(self) -> str:
        return os.getenv("LOGGING_LEVEL", "INFO").upper()

    @property
    def heartbeat_check_url(self) -> str | None:
        return os.getenv("HEARTBEAT_CHECK_URL")

    @property
    def heartbeat_interval(self) -> str:
        return os.getenv("HEARTBEAT_INTERVAL", "*/5")

    @property
    def refresh_completed_url(self) -> str | None:
        return os.getenv("REFRESH_COMPLETED_URL")

    @cached_property
    def open_exchange_rates_app_id(self) -> str | None:
        if self.is_test:
            return "FAKE_OER_APP_ID"

        return os.getenv("OPEN_EXCHANGE_RATES_APP_ID")

    @property
    def exchange_rates_refresh_hour(self) -> str:
        return os.getenv("EXCHANGE_RATES_REFRESH_HOUR", "13")

    @property
    def exchange_rates_refresh_minute(self) -> str:
        return os.getenv("EXCHANGE_RATES_REFRESH_MINUTE", "00")

    @cached_property
    def DATABASE_URL(self) -> str:
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "postgres")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB", "exchange_house_development")

        if not all([user, password, host, db_name]):
            raise ValueError("Missing required database environment variables")

        return f"asyncpg://{user}:{password}@{host}:{port}/{db_name}"


settings = Settings()
