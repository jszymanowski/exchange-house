import os
from functools import cached_property

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Exchange House"
    PROJECT_DESCRIPTION: str = "A simple API for exchange rates"
    PROJECT_VERSION: str = "v1"

    @cached_property
    def environment(self) -> str:
        return os.getenv("ENV", "development")

    @property
    def is_test(self) -> bool:
        return self.environment == "test"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @cached_property
    def timezone(self) -> str:
        return os.getenv("TZ", "UTC")

    @cached_property
    def debug_mode(self) -> bool:
        return os.getenv("DEBUG_MODE", "false").lower() == "true"

    @cached_property
    def log_level(self) -> str:
        default_log_level = "DEBUG" if self.debug_mode else "INFO"
        return os.getenv("LOG_LEVEL", default_log_level).upper()

    @cached_property
    def open_exchange_rates_app_id(self) -> str | None:
        if self.is_test:
            return "FAKE_OER_APP_ID"

        return os.getenv("OPEN_EXCHANGE_RATES_APP_ID")

    @cached_property
    def database_url(self) -> str:
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "postgres")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB", "exchange_house_development")

        if not all([user, password, host, db_name]):
            raise ValueError("Missing required database environment variables")

        return f"asyncpg://{user}:{password}@{host}:{port}/{db_name}"


settings = Settings()


class EmailSettings(BaseSettings):
    @property
    def is_configured(self) -> bool:
        return all([self.smtp_server, self.smtp_port, self.smtp_username, self.smtp_password])

    @cached_property
    def smtp_server(self) -> str | None:
        return os.getenv("SMTP_SERVER")

    @cached_property
    def smtp_port(self) -> int:
        return int(os.getenv("SMTP_PORT", "587"))

    @cached_property
    def smtp_username(self) -> str | None:
        return os.getenv("SMTP_USERNAME")

    @cached_property
    def smtp_password(self) -> str | None:
        return os.getenv("SMTP_PASSWORD")

    @cached_property
    def admin_email(self) -> str | None:
        return os.getenv("ADMIN_EMAIL")


email_settings = EmailSettings()


class CelerySettings(BaseSettings):
    @cached_property
    def redis_host(self) -> str:
        return os.getenv("REDIS_HOST", "localhost")

    @cached_property
    def redis_port(self) -> str:
        return os.getenv("REDIS_PORT", "6379")

    @property
    def celery_broker_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"

    @property
    def celery_backend_url(self) -> str:
        return self.celery_broker_url

    @cached_property
    def flower_port(self) -> int:
        return int(os.getenv("FLOWER_PORT", "5555"))

    @cached_property
    def heartbeat_interval(self) -> str:
        return os.getenv("HEARTBEAT_INTERVAL", "*/5")

    @cached_property
    def exchange_rates_refresh_hour(self) -> str:
        return os.getenv("EXCHANGE_RATES_REFRESH_HOUR", "13")

    @cached_property
    def exchange_rates_refresh_minute(self) -> str:
        return os.getenv("EXCHANGE_RATES_REFRESH_MINUTE", "00")

    @property
    def timezone(self) -> str:
        return settings.timezone


celery_settings = CelerySettings()


class HealthcheckSettings(BaseSettings):
    @cached_property
    def heartbeat_check_url(self) -> str | None:
        return os.getenv("HEARTBEAT_CHECK_URL")

    @cached_property
    def refresh_completed_url(self) -> str | None:
        return os.getenv("REFRESH_COMPLETED_URL")


healthcheck_settings = HealthcheckSettings()


class FirebaseSettings(BaseSettings):
    @cached_property
    def firebase_credentials_path(self) -> str | None:
        if settings.is_test:
            return None

        credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
        if not credentials_path:
            raise ValueError("FIREBASE_CREDENTIALS_PATH environment variable is required")

        return credentials_path

    @cached_property
    def base_currency_code(self) -> str:
        return os.getenv("BASE_CURRENCY_CODE", "USD")


firebase_settings = FirebaseSettings()
