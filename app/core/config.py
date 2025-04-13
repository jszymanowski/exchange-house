import os
from functools import cached_property

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    @cached_property
    def DATABASE_URL(self) -> str:
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST")
        port = os.getenv("POSTGRES_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB")

        if not all([user, password, host, db_name]):
            raise ValueError("Missing required database environment variables")

        return f"asyncpg://{user}:{password}@{host}:{port}/{db_name}"


settings = Settings()
