from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router as api_router
from app.core.database import register_orm


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    # app startup
    try:
        async with register_orm(app):
            # db connected
            yield
            # app teardown
        # db connections closed
    except Exception as e:
        # TODO: log this, once a logger is added
        print(f"Database connection error: {e}")
        raise


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
