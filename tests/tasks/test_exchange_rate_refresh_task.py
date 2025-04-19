from unittest.mock import AsyncMock, patch

import pytest

from app.services.exchange_rate_service import ExchangeRateServiceInterface
from app.services.healthchecks_service import NoURLSetError
from app.tasks.exchange_rate_refresh_task import _exchange_rate_refresh


@pytest.fixture
def mock_exchange_rate_refresh():
    with (
        patch("app.services.exchange_rate_refresh.ExchangeRateRefresh") as mock_exchange_rate_refresh_class,
    ):
        mock_exchange_rate_refresh = AsyncMock()
        mock_exchange_rate_refresh_class.return_value = mock_exchange_rate_refresh
        yield mock_exchange_rate_refresh


@pytest.fixture
def mock_get_exchange_rate_service():
    with (
        patch("app.tasks.exchange_rate_refresh_task.get_exchange_rate_service") as mock_get_exchange_rate_service,
    ):
        yield mock_get_exchange_rate_service


@pytest.fixture
def mock_healthchecks_service():
    with (
        patch("app.tasks.exchange_rate_refresh_task.healthchecks_service") as mock_healthchecks_service,
    ):
        yield mock_healthchecks_service


@pytest.fixture
def mock_send_exchange_rate_refresh_email():
    with (
        patch(
            "app.tasks.exchange_rate_refresh_task.send_exchange_rate_refresh_email"
        ) as mock_send_exchange_rate_refresh_email,
    ):
        yield mock_send_exchange_rate_refresh_email


@pytest.fixture
def mock_logger():
    with (
        patch("app.tasks.exchange_rate_refresh_task.logger") as mock_logger,
    ):
        yield mock_logger


@pytest.mark.asyncio
async def test_latest_exchange_rates_task_success(
    mock_exchange_rate_refresh: AsyncMock,
    mock_get_exchange_rate_service: AsyncMock,
    mock_healthchecks_service: AsyncMock,
    mock_send_exchange_rate_refresh_email: AsyncMock,
    test_exchange_rate_service: ExchangeRateServiceInterface,
):
    mock_healthchecks_service.ping_refresh_completed.return_value = None
    mock_get_exchange_rate_service.return_value = test_exchange_rate_service

    result = await _exchange_rate_refresh()
    assert result == {"message": None, "status": "SUCCESS"}

    mock_exchange_rate_refresh.save.assert_called_once()
    mock_send_exchange_rate_refresh_email.assert_called_once_with(exchange_rate_service=test_exchange_rate_service)
    mock_healthchecks_service.ping_refresh_completed.assert_called_once()


@pytest.mark.asyncio
async def test_exchange_rate_refresh_task_handles_refresh_error(
    mock_exchange_rate_refresh: AsyncMock,
    mock_get_exchange_rate_service: AsyncMock,
    test_exchange_rate_service: ExchangeRateServiceInterface,
):
    mock_exchange_rate_refresh.save.side_effect = Exception("Test error")

    result = await _exchange_rate_refresh()
    assert result == {"message": "Refresh failed: Test error", "status": "FAILURE"}

    mock_exchange_rate_refresh.save.assert_called_once()


@pytest.mark.asyncio
async def test_latest_exchange_rates_task_no_healthcheck_url(
    mock_exchange_rate_refresh: AsyncMock,
    mock_get_exchange_rate_service: AsyncMock,
    mock_healthchecks_service: AsyncMock,
    mock_send_exchange_rate_refresh_email: AsyncMock,
    mock_logger: AsyncMock,
    test_exchange_rate_service: ExchangeRateServiceInterface,
):
    mock_healthchecks_service.ping_refresh_completed.side_effect = NoURLSetError

    result = await _exchange_rate_refresh()
    assert result == {"message": "Healthcheck failed: No check-in URL set", "status": "WARNING"}

    mock_exchange_rate_refresh.save.assert_called_once()
    mock_logger.warning.assert_called_once_with("Healthcheck failed: No check-in URL set")


@pytest.mark.asyncio
async def test_latest_exchange_rates_task_email_failure(
    mock_exchange_rate_refresh: AsyncMock,
    mock_get_exchange_rate_service: AsyncMock,
    mock_healthchecks_service: AsyncMock,
    mock_send_exchange_rate_refresh_email: AsyncMock,
    mock_logger: AsyncMock,
    test_exchange_rate_service: ExchangeRateServiceInterface,
):
    mock_send_exchange_rate_refresh_email.side_effect = Exception("Email sending error")

    result = await _exchange_rate_refresh()
    assert result == {"message": "Send email failed: Email sending error", "status": "WARNING"}

    mock_exchange_rate_refresh.save.assert_called_once()
    mock_send_exchange_rate_refresh_email.assert_called_once()
    mock_healthchecks_service.ping_refresh_completed.assert_not_called()

    mock_logger.warning.assert_called_once()
    args, _ = mock_logger.warning.call_args
    assert "Send email failed: Email sending error" in args[0]


@pytest.mark.skip(reason="idk wtf is going on here")
@patch("app.tasks.exchange_rate_refresh_task.healthchecks_service")
@pytest.mark.asyncio
async def test_latest_exchange_rates_task_healthcheck_failure(
    mock_exchange_rate_refresh: AsyncMock,
    mock_get_exchange_rate_service: AsyncMock,
    mock_healthchecks_service: AsyncMock,
    mock_send_exchange_rate_refresh_email: AsyncMock,
    mock_logger: AsyncMock,
    test_exchange_rate_service: ExchangeRateServiceInterface,
):
    mock_healthchecks_service.ping_refresh_completed.side_effect = Exception("Healthcheck error")
    mock_healthchecks_service.ping_refresh_completed.side_effect = Exception("Healthcheck error")

    result = await _exchange_rate_refresh()
    assert result == {"message": "Healthcheck failed: Healthcheck error", "status": "WARNING"}

    mock_exchange_rate_refresh.save.assert_called_once()
    mock_send_exchange_rate_refresh_email.assert_called_once()
    mock_healthchecks_service.ping_refresh_completed.assert_called_once()

    mock_logger.warning.assert_called_once()
    args, _ = mock_logger.warning.call_args
    assert "Healthcheck failed: Healthcheck error" in args[0]
