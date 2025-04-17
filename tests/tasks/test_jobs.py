from unittest.mock import AsyncMock, patch

import pytest

from app.services.exchange_rate_service import ExchangeRateServiceInterface
from app.tasks.exchange_rate_refresh_task import latest_exchange_rates_task
from tests.support.database_helper import DatabaseTestHelper


@pytest.mark.asyncio
async def test_latest_exchange_rates_task_success(
    test_database: DatabaseTestHelper, test_exchange_rate_service: ExchangeRateServiceInterface
):
    with (
        patch("app.tasks.jobs.ExchangeRateRefresh") as mock_exchange_rate_refresh_class,
        patch("app.tasks.jobs.send_exchange_rate_refresh_email") as mock_send_email,
        patch("app.tasks.jobs.get_healthchecks_client") as mock_get_healthchecks_client,
        patch("app.tasks.jobs.settings") as mock_settings,
    ):
        mock_exchange_rate_refresh = AsyncMock()
        mock_exchange_rate_refresh_class.return_value = mock_exchange_rate_refresh

        mock_healthchecks_client = AsyncMock()
        mock_get_healthchecks_client.return_value = mock_healthchecks_client

        mock_settings.refresh_completed_url = "http://example.com/ping"

        await latest_exchange_rates_task(exchange_rate_service=test_exchange_rate_service)

        mock_exchange_rate_refresh_class.assert_called_once_with(exchange_rate_service=test_exchange_rate_service)
        mock_exchange_rate_refresh.save.assert_called_once()

        mock_send_email.assert_called_once_with(exchange_rate_service=test_exchange_rate_service)

        mock_get_healthchecks_client.assert_called_once()
        mock_healthchecks_client.ping.assert_called_once_with(mock_settings.refresh_completed_url)


@pytest.mark.asyncio
async def test_latest_exchange_rates_task_no_healthcheck_url(
    test_database: DatabaseTestHelper, test_exchange_rate_service: ExchangeRateServiceInterface
):
    with (
        patch("app.tasks.jobs.ExchangeRateRefresh") as mock_exchange_rate_refresh_class,
        patch("app.tasks.jobs.send_exchange_rate_refresh_email") as mock_send_email,
        patch("app.tasks.jobs.get_healthchecks_client") as mock_get_healthchecks_client,
        patch("app.tasks.jobs.settings") as mock_settings,
        patch("app.tasks.jobs.metrics") as mock_metrics,
        patch("app.tasks.jobs.logger") as mock_logger,
    ):
        mock_exchange_rate_refresh = AsyncMock()
        mock_exchange_rate_refresh_class.return_value = mock_exchange_rate_refresh

        mock_settings.refresh_completed_url = None

        await latest_exchange_rates_task(exchange_rate_service=test_exchange_rate_service)

        mock_metrics.record_job_start.assert_called_once_with("exchange_rate_notification")

        mock_exchange_rate_refresh_class.assert_called_once_with(exchange_rate_service=test_exchange_rate_service)
        mock_exchange_rate_refresh.save.assert_called_once()

        mock_send_email.assert_called_once_with(exchange_rate_service=test_exchange_rate_service)

        mock_get_healthchecks_client.assert_not_called()
        mock_logger.warning.assert_called_once_with("Refresh completed, but check-in failed: URL is not set")


@pytest.mark.asyncio
async def test_latest_exchange_rates_task_refresh_failure(
    test_database: DatabaseTestHelper, test_exchange_rate_service: ExchangeRateServiceInterface
):
    with (
        patch("app.tasks.jobs.ExchangeRateRefresh") as mock_exchange_rate_refresh_class,
        patch("app.tasks.jobs.send_exchange_rate_refresh_email") as mock_send_email,
        patch("app.tasks.jobs.get_healthchecks_client") as mock_get_healthchecks_client,
        patch("app.tasks.jobs.metrics") as mock_metrics,
        patch("app.tasks.jobs.logger") as mock_logger,
    ):
        mock_exchange_rate_refresh = AsyncMock()
        mock_exchange_rate_refresh.save.side_effect = Exception("Test exception")
        mock_exchange_rate_refresh_class.return_value = mock_exchange_rate_refresh

        await latest_exchange_rates_task(exchange_rate_service=test_exchange_rate_service)

        mock_metrics.record_job_start.assert_called_once_with("exchange_rate_notification")

        mock_exchange_rate_refresh_class.assert_called_once_with(exchange_rate_service=test_exchange_rate_service)
        mock_exchange_rate_refresh.save.assert_called_once()

        mock_send_email.assert_not_called()
        mock_get_healthchecks_client.assert_not_called()

        mock_logger.error.assert_called_once_with("Exchange rate refresh failed: Test exception")


@pytest.mark.asyncio
async def test_latest_exchange_rates_task_email_failure(
    test_database: DatabaseTestHelper, test_exchange_rate_service: ExchangeRateServiceInterface
):
    with (
        patch("app.tasks.jobs.ExchangeRateRefresh") as mock_exchange_rate_refresh_class,
        patch("app.tasks.jobs.send_exchange_rate_refresh_email") as mock_send_email,
        patch("app.tasks.jobs.get_healthchecks_client") as mock_get_healthchecks_client,
        patch("app.tasks.jobs.metrics") as mock_metrics,
        patch("app.tasks.jobs.logger") as mock_logger,
    ):
        mock_exchange_rate_refresh = AsyncMock()
        mock_exchange_rate_refresh_class.return_value = mock_exchange_rate_refresh

        email_error = Exception("Email sending error")
        mock_send_email.side_effect = email_error

        await latest_exchange_rates_task(exchange_rate_service=test_exchange_rate_service)

        mock_metrics.record_job_start.assert_called_once_with("exchange_rate_notification")

        mock_exchange_rate_refresh_class.assert_called_once_with(exchange_rate_service=test_exchange_rate_service)
        mock_exchange_rate_refresh.save.assert_called_once()
        mock_send_email.assert_called_once()

        mock_get_healthchecks_client.assert_not_called()

        mock_logger.error.assert_called_once()
        args, _ = mock_logger.error.call_args
        assert "Email sending error" in args[0]


@pytest.mark.asyncio
async def test_latest_exchange_rates_task_healthcheck_failure(
    test_database: DatabaseTestHelper, test_exchange_rate_service: ExchangeRateServiceInterface
):
    with (
        patch("app.tasks.jobs.ExchangeRateRefresh") as mock_exchange_rate_refresh_class,
        patch("app.tasks.jobs.send_exchange_rate_refresh_email") as mock_send_email,
        patch("app.tasks.jobs.get_healthchecks_client") as mock_get_healthchecks_client,
        patch("app.tasks.jobs.settings") as mock_settings,
        patch("app.tasks.jobs.logger") as mock_logger,
    ):
        mock_exchange_rate_refresh = AsyncMock()
        mock_exchange_rate_refresh_class.return_value = mock_exchange_rate_refresh

        mock_healthchecks_client = AsyncMock()
        mock_healthchecks_client.ping.side_effect = Exception("Healthcheck error")
        mock_get_healthchecks_client.return_value = mock_healthchecks_client

        mock_settings.refresh_completed_url = "http://example.com/ping"

        await latest_exchange_rates_task(exchange_rate_service=test_exchange_rate_service)

        mock_exchange_rate_refresh_class.assert_called_once_with(exchange_rate_service=test_exchange_rate_service)
        mock_exchange_rate_refresh.save.assert_called_once()
        mock_send_email.assert_called_once()

        mock_get_healthchecks_client.assert_called_once()
        mock_healthchecks_client.ping.assert_called_once()

        mock_logger.error.assert_called_once()
        args, _ = mock_logger.error.call_args
        assert "Healthcheck failed: Healthcheck error" in args[0]
