import logging
import sys
from logging import Handler
from pathlib import Path

from app.core.config import settings


def setup_logging() -> None:
    try:
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        logging_level = settings.logging_level
        handlers: list[Handler] = [logging.FileHandler(f"logs/{settings.environment}.log")]
        if not settings.is_test:
            handlers.append(logging.StreamHandler(sys.stdout))
        logging.basicConfig(
            level=logging_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=handlers,
        )
    except Exception as e:
        # Fallback to basic console logging if setup fails
        print(f"Error setting up logging: {e}")
        logging.basicConfig(
            level="INFO",
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )


logger = logging.getLogger("exchange-house")
