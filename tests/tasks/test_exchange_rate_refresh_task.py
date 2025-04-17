from unittest.mock import AsyncMock, patch

import pytest

from app.models import ExchangeRate
from app.services.exchange_rate_service import ExchangeRateServiceInterface
from app.tasks.exchange_rate_refresh_task import _exchange_rate_refresh
from tests.support.database_helper import DatabaseTestHelper


@pytest.mark.skip(reason="remove")
@pytest.mark.asyncio
async def test_exchange_rate_refresh_task_integration():
    """Test the task through Celery's API."""
    # Mock any external services
    with patch("app.tasks.exchange_rate_refresh_task.get_exchange_rate_service") as mock_service:
        mock_service.return_value.get_latest_rates.return_value = {"USD": 1.0, "EUR": 0.85, "GBP": 0.75}

        # Call the task through Celery
        result = await _exchange_rate_refresh()

        # In eager mode, the result is available immediately
        assert result == "Success"

        # Verify database operations
        rates = await ExchangeRate.all()
        assert len(rates) > 0


@pytest.mark.asyncio
async def test_latest_exchange_rates_task_success(
    test_database: DatabaseTestHelper, test_exchange_rate_service: ExchangeRateServiceInterface
):
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
        assert result == "Success"

        mock_exchange_rate_refresh_class.assert_called_once_with(exchange_rate_service=test_exchange_rate_service)
        mock_exchange_rate_refresh.save.assert_called_once()

        mock_send_email.assert_called_once_with(exchange_rate_service=test_exchange_rate_service)

        mock_get_healthchecks_client.assert_called_once()
        mock_healthchecks_client.ping.assert_called_once_with(mock_settings.refresh_completed_url)
