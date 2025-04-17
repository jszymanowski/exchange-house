import asyncio
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from typing import Any

from fastapi import BackgroundTasks

# Create a shared thread pool executor for I/O bound tasks
_thread_pool = ThreadPoolExecutor()


def perform_as_background_task(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to make a function run in the background.
    Works both in FastAPI routes and scheduled tasks.
    """

    @wraps(func)
    def wrapper(*args: Any, background_tasks: BackgroundTasks | None = None, **kwargs: Any) -> None:
        # If we're in a FastAPI route with dependency injection
        if background_tasks is not None:
            background_tasks.add_task(func, *args, **kwargs)
        # If we're in a scheduled job or directly called
        else:
            # Use a thread for blocking I/O operations
            loop = asyncio.get_event_loop()
            loop.run_in_executor(_thread_pool, lambda: func(*args, **kwargs))

        return None

    return wrapper
