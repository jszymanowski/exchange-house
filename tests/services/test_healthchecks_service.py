from unittest.mock import AsyncMock

import pytest
from httpx import Response

from app.core.config import healthcheck_settings
from app.services.healthchecks_service import HealthchecksService, HealthchecksServiceError


@pytest.fixture
def mock_healthchecks_client() -> AsyncMock:
    mock = AsyncMock()
    mock.ping.return_value = Response(status_code=200)
    return mock


@pytest.mark.asyncio
async def test_ping_heartbeat_success(mock_healthchecks_client: AsyncMock) -> None:
    await HealthchecksService(client=mock_healthchecks_client).ping_heartbeat()
    mock_healthchecks_client.ping.assert_called_once_with(healthcheck_settings.heartbeat_check_url)


@pytest.mark.asyncio
async def test_ping_heartbeat_failure(mock_healthchecks_client: AsyncMock) -> None:
    mock_healthchecks_client.ping.side_effect = Exception("Test error")

    with pytest.raises(HealthchecksServiceError):
        await HealthchecksService(client=mock_healthchecks_client).ping_heartbeat()


@pytest.mark.asyncio
async def test_ping_refresh_completed_success(mock_healthchecks_client: AsyncMock) -> None:
    await HealthchecksService(client=mock_healthchecks_client).ping_refresh_completed()
    mock_healthchecks_client.ping.assert_called_once_with(healthcheck_settings.refresh_completed_url)


@pytest.mark.asyncio
async def test_ping_refresh_completed_failure(mock_healthchecks_client: AsyncMock) -> None:
    mock_healthchecks_client.ping.side_effect = Exception("Test error")

    with pytest.raises(HealthchecksServiceError):
        await HealthchecksService(client=mock_healthchecks_client).ping_refresh_completed()
