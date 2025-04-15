import logging
import os
import sys
from logging import Handler
from pathlib import Path

from app.core.config import settings


def setup_logging() -> None:
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logging_level = os.getenv("LOGGING_LEVEL", "INFO").upper()

    handlers: list[Handler] = [logging.FileHandler(f"logs/{settings.environment}.log")]
    if settings.environment != "test":
        handlers.append(logging.StreamHandler(sys.stdout))

    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )


logger = logging.getLogger("exchange-house")
