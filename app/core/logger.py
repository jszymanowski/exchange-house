import json
import logging
import sys
from datetime import datetime
from logging import Handler
from pathlib import Path
from typing import Any, Literal

from app.core.config import settings

type LogDomain = Literal["default", "celery", "email", "rate_refresh", "heartbeat"]


class JSONLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        try:
            simple_path = record.pathname.split("/app/")[-1]
        except Exception:
            simple_path = record.pathname

        log_record: dict[str, Any] = {
            "domain": record.name,
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "path": simple_path,
            "line": record.lineno,
        }

        # Include exception info if present
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        # Include any extra attributes
        if hasattr(record, "extra"):
            log_record.update(record.extra)

        return json.dumps(log_record)


def setup_logging() -> None:
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    log_level = settings.log_level

    handlers: list[Handler] = [logging.FileHandler(f"logs/{settings.environment}.log")]

    if not settings.is_test:
        handlers.append(logging.StreamHandler(sys.stdout))

    if settings.is_production:
        format = ""
        for handler in handlers:
            handler.setFormatter(JSONLogFormatter())
    else:
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=log_level,
        format=format,
        handlers=handlers,
    )


def get_logger(name: LogDomain) -> logging.Logger:
    return logging.getLogger(name)


default_logger = logging.getLogger("default")
