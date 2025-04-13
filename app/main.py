from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import register_orm


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    # app startup
    async with register_orm(app):
        # db connected
        yield
        # app teardown
    # db connections closed


app = FastAPI(lifespan=lifespan)
