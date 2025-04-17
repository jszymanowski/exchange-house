from unittest.mock import AsyncMock, patch

import pytest

from app.services.exchange_rate_service import ExchangeRateServiceInterface
from app.tasks.exchange_rate_refresh_task import _exchange_rate_refresh


@pytest.mark.asyncio
async def test_latest_exchange_rates_task_success(test_exchange_rate_service: ExchangeRateServiceInterface):
    with (
        patch("app.tasks.exchange_rate_refresh_task.ExchangeRateRefresh") as mock_exchange_rate_refresh_class,
        patch("app.tasks.exchange_rate_refresh_task.send_exchange_rate_refresh_email") as mock_send_email,
        patch("app.tasks.exchange_rate_refresh_task.get_healthchecks_client") as mock_get_healthchecks_client,
        patch("app.tasks.exchange_rate_refresh_task.settings") as mock_settings,
        patch("app.tasks.exchange_rate_refresh_task.get_exchange_rate_service") as mock_get_exchange_rate_service,
    ):
        mock_exchange_rate_refresh = AsyncMock()
        mock_exchange_rate_refresh_class.return_value = mock_exchange_rate_refresh

        mock_healthchecks_client = AsyncMock()
        mock_get_healthchecks_client.return_value = mock_healthchecks_client

        mock_get_exchange_rate_service.return_value = test_exchange_rate_service

        mock_settings.refresh_completed_url = "http://example.com/ping"

        result = await _exchange_rate_refresh()
        assert result == {"message": None, "status": "SUCCESS"}

        mock_exchange_rate_refresh_class.assert_called_once_with(exchange_rate_service=test_exchange_rate_service)
        mock_exchange_rate_refresh.save.assert_called_once()

        mock_send_email.assert_called_once_with(exchange_rate_service=test_exchange_rate_service)

        mock_get_healthchecks_client.assert_called_once()
        mock_healthchecks_client.ping.assert_called_once_with(mock_settings.refresh_completed_url)


@pytest.mark.asyncio
async def test_exchange_rate_refresh_task_handles_refresh_errors(
    test_exchange_rate_service: ExchangeRateServiceInterface,
):
    with (
        patch("app.tasks.exchange_rate_refresh_task.ExchangeRateRefresh") as mock_exchange_rate_refresh_class,
        patch("app.tasks.exchange_rate_refresh_task.get_exchange_rate_service") as mock_get_exchange_rate_service,
    ):
        mock_exchange_rate_refresh = AsyncMock()
        mock_exchange_rate_refresh.save.side_effect = Exception("Test error")
        mock_exchange_rate_refresh_class.return_value = mock_exchange_rate_refresh

        mock_get_exchange_rate_service.return_value = test_exchange_rate_service

        # Should still complete without raising exception
        result = await _exchange_rate_refresh()
        assert result == {"message": "Test error", "status": "FAILURE"}

        # Verify connections were closed even with the error
        mock_exchange_rate_refresh.save.assert_called_once()
