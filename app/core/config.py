import os
from functools import cached_property

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    @property
    def environment(self) -> str:
        return os.getenv("ENV", "development")

    @property
    def is_test(self) -> bool:
        return self.environment == "test"

    @property
    def database_name(self) -> str:
        return os.getenv("POSTGRES_DB", "exchange_house_development")

    @cached_property
    def DATABASE_URL(self) -> str:
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "postgres")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        db_name = self.database_name

        if not all([user, password, host, db_name]):
            raise ValueError("Missing required database environment variables")

        return f"asyncpg://{user}:{password}@{host}:{port}/{db_name}"


settings = Settings()
