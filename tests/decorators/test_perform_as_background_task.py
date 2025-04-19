import asyncio
import time
from unittest.mock import MagicMock

import pytest
from fastapi import BackgroundTasks

from app.decorators.perform_as_background_task import perform_as_background_task


@pytest.mark.asyncio
async def test_function_with_background_tasks() -> None:
    """Test decorator with BackgroundTasks injected"""
    test_function = MagicMock()
    background_tasks = BackgroundTasks()

    @perform_as_background_task
    def decorated_function(arg1: str, arg2: str, kwarg1: str | None = None) -> None:
        test_function(arg1, arg2, kwarg1=kwarg1)

    # Call with background_tasks
    decorated_function("value1", "value2", background_tasks=background_tasks, kwarg1="kwvalue")

    # Verify function wasn't called yet (only added to background tasks)
    test_function.assert_not_called()

    # Run background tasks - need to await each task
    for task in background_tasks.tasks:
        await task()

    # Now verify the function was called with correct args
    test_function.assert_called_once_with("value1", "value2", kwarg1="kwvalue")


@pytest.mark.asyncio
async def test_function_without_background_tasks() -> None:
    """Test decorator without BackgroundTasks (scheduled job scenario)"""
    test_function = MagicMock()

    @perform_as_background_task
    def decorated_function(arg1: str, arg2: str, kwarg1: str | None = None) -> None:
        test_function(arg1, arg2, kwarg1=kwarg1)

    # Call without background_tasks
    decorated_function("value1", "value2", kwarg1="kwvalue")

    # Function should run in a thread, give it a moment to complete
    await asyncio.sleep(0.1)

    # Verify the function was called
    test_function.assert_called_once_with("value1", "value2", kwarg1="kwvalue")


@pytest.mark.asyncio
async def test_thread_execution() -> None:
    """Test that function actually runs in a separate thread"""
    current_thread_ids = []

    def get_thread_id() -> int:
        import threading

        return threading.get_ident()

    # Get current thread ID
    main_thread_id = get_thread_id()
    current_thread_ids.append(main_thread_id)

    @perform_as_background_task
    def thread_function() -> None:
        # Get the thread ID inside the function
        thread_id = get_thread_id()
        current_thread_ids.append(thread_id)
        # Simulate some work
        time.sleep(0.1)

    # Call function (should run in background thread)
    thread_function()

    # Wait for thread to complete
    await asyncio.sleep(0.2)

    # Should have two different thread IDs
    assert len(current_thread_ids) == 2
    assert current_thread_ids[0] != current_thread_ids[1]


@pytest.mark.asyncio
async def test_function_result() -> None:
    """Test that the decorator always returns None regardless of function return value"""

    @perform_as_background_task
    def function_with_return() -> None:
        return "some result"

    # With background tasks
    background_tasks = BackgroundTasks()
    result1 = function_with_return(background_tasks=background_tasks)
    assert result1 is None

    # Without background tasks
    result2 = function_with_return()
    assert result2 is None


@pytest.mark.asyncio
async def test_exception_handling() -> None:
    """Test that exceptions in the background function don't propagate"""
    error_raised = False

    @perform_as_background_task
    def function_with_exception() -> None:
        nonlocal error_raised
        error_raised = True
        raise ValueError("Test exception")

    # Call function (should not raise exception to caller)
    try:
        function_with_exception()
        await asyncio.sleep(0.1)  # Give thread time to execute
        assert error_raised  # Confirm function did run and raise error internally
    except ValueError:
        pytest.fail("Exception should not propagate to caller")


@pytest.mark.asyncio
async def test_with_fastapi_route() -> None:
    """Test integration with FastAPI routes"""
    test_function = MagicMock()

    @perform_as_background_task
    def task_function(arg1: str) -> None:
        test_function(arg1)

    # Simulate FastAPI dependency injection
    background_tasks = BackgroundTasks()

    # This mimics a FastAPI route that injects BackgroundTasks
    async def route_handler(background_tasks: BackgroundTasks = background_tasks) -> dict[str, str]:
        task_function("test_value", background_tasks=background_tasks)
        return {"status": "scheduled"}

    # Call the route handler
    await route_handler(background_tasks)

    # Verify function wasn't called immediately
    test_function.assert_not_called()

    # Execute background tasks - need to await each task
    for task in background_tasks.tasks:
        await task()

    # Verify function was called with correct args
    test_function.assert_called_once_with("test_value")
