from collections.abc import Callable
from functools import wraps
from typing import Any

from tortoise import Tortoise
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.transactions import atomic


def database_transactional(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to make a function transactional when used alone,
    but able to participate in a parent transaction when nested.

    If an exception occurs, the transaction will be automatically rolled back.
    """

    @wraps(func)
    async def wrapper(*args: Any, db_connection: BaseDBAsyncClient | None = None, **kwargs: Any) -> Any:
        if db_connection:
            # Already in a transaction, just execute the function
            return await func(*args, db_connection=db_connection, **kwargs)
        else:
            # Start a new transaction
            @atomic()
            async def run_in_transaction() -> Any:
                conn = Tortoise.get_connection("default")
                return await func(*args, db_connection=conn, **kwargs)

            return await run_in_transaction()

    return wrapper
