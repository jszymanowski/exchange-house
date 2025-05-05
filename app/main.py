import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import tortoise_exception_handlers

from app.api.routes import router as api_router
from app.core.config import settings
from app.core.database import register_orm
from app.core.logger import default_logger, setup_logging
from app.middleware.logging import LoggingMiddleware


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
                yield
                # app teardown
            # db connections closed
        except Exception as e:
            default_logger.error(f"Database connection error: {e}")
            raise


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
    exception_handlers=tortoise_exception_handlers(),
)

app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(api_router)

FRONTEND_DIR = "app/frontend/build"
if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")
else:
    from fastapi.responses import RedirectResponse

    @app.get("/")
    async def redirect_to_docs() -> RedirectResponse:
        return RedirectResponse(url="/docs")
