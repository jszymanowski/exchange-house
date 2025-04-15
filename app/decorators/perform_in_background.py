from collections.abc import Callable
from functools import wraps
from typing import Any

from fastapi import BackgroundTasks


def perform_in_background(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to make a function run in the background.
    """

    @wraps(func)
    async def wrapper(*args: Any, background_tasks: BackgroundTasks, **kwargs: Any) -> Any:
        background_tasks.add_task(func, *args, **kwargs)

    return wrapper
