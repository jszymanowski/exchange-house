import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import default_logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        request_id = str(uuid.uuid4())
        method = request.method
        url = request.url.path

        start_time = time.time()

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        # Build log data
        process_time_ms = round((time.time() - start_time) * 1000, 2)
        log_data = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "query_params": str(request.query_params),
            "client_ip": request.client.host if request.client else None,
            "process_time_ms": process_time_ms,
            "status_code": response.status_code,
        }

        default_logger.info(
            f"Request to {method} {url} completed in {process_time_ms}ms with status {response.status_code}",
            extra={"extra": log_data},
        )

        return response
