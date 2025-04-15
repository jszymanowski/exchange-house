from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise.contrib.fastapi import tortoise_exception_handlers

from app.api.routes import admin_router
from app.api.routes import router as api_router
from app.core.config import settings
from app.core.database import register_orm
from app.core.jobs import scheduler_manager
from app.core.logger import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    if settings.is_test:
        yield
        return
    else:
        # app startup
        setup_logging()
        try:
            async with register_orm(app):
                # db connected
                await scheduler_manager.start()

                yield

                await scheduler_manager.shutdown()
                # app teardown
            # db connections closed
        except Exception as e:
            # TODO: log this, once a logger is added
            print(f"Database connection error: {e}")
            raise


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
    exception_handlers=tortoise_exception_handlers(),
)

app.include_router(api_router)
app.include_router(admin_router)
