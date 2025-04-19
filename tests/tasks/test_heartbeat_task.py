from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest

from app.tasks.heartbeat_task import NoURLSetError, _heartbeat_task


@pytest.fixture
def mock_healthchecks_service() -> Generator[AsyncMock]:
    with (
        patch("app.tasks.heartbeat_task.get_healthchecks_service", new_callable=AsyncMock) as mock,
    ):
        yield mock


@pytest.mark.asyncio
async def test_heartbeat_task_success(mock_healthchecks_service: AsyncMock):
    mock_healthchecks_service.ping_heartbeat.return_value = None

    result = await _heartbeat_task()
    assert result == {"message": None, "status": "SUCCESS"}

    mock_healthchecks_service.ping_heartbeat.assert_called_once()


@pytest.mark.asyncio
async def test_heartbeat_task_skipped(mock_healthchecks_service: AsyncMock):
    mock_healthchecks_service.ping_heartbeat.side_effect = NoURLSetError

    result = await _heartbeat_task()
    assert result == {"message": "Heartbeat completed, but no check-in URL set", "status": "SKIPPED"}

    mock_healthchecks_service.ping_heartbeat.assert_called_once()


@pytest.mark.asyncio
async def test_heartbeat_task_failure(mock_healthchecks_service: AsyncMock):
    mock_healthchecks_service.ping_heartbeat.side_effect = Exception("Test error")

    result = await _heartbeat_task()
    assert result == {"message": "Heartbeat completed, but check-in failed: Test error", "status": "FAILURE"}

    mock_healthchecks_service.ping_heartbeat.assert_called_once()
