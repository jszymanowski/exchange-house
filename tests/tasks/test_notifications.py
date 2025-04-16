from datetime import date
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models import Currency
from app.services.exchange_rate_service import ExchangeRateServiceInterface
from app.tasks.notifications import send_exchange_rate_refresh_email
from tests.support.factories import build_exchange_rate


@pytest.mark.asyncio
async def test_send_exchange_rate_refresh_email_success():
    mock_exchange_rate_service = MagicMock(spec=ExchangeRateServiceInterface)

    latest_rate = build_exchange_rate(
        as_of=date(2024, 5, 2), base_currency_code="SGD", quote_currency_code="USD", rate=Decimal("0.75")
    )

    previous_rate = build_exchange_rate(
        as_of=date(2024, 5, 1), base_currency_code="SGD", quote_currency_code="USD", rate=Decimal("0.72")
    )

    mock_exchange_rate_service.get_historical_rates.return_value = [latest_rate, previous_rate]

    with (
        patch("app.tasks.notifications.email_settings") as mock_email_settings,
        patch("app.tasks.notifications.EmailService") as mock_email_service_class,
    ):
        mock_email_settings.admin_email = "admin@example.com"

        mock_email_service = MagicMock()
        mock_email_service_class.return_value = mock_email_service

        await send_exchange_rate_refresh_email(exchange_rate_service=mock_exchange_rate_service)

        mock_exchange_rate_service.get_historical_rates.assert_called_once_with(
            base_currency_code=Currency("SGD"), quote_currency_code=Currency("USD"), limit=2, sort_order="desc"
        )

        expected_subject = f"[ExchangeHouse] Exchange rates for {latest_rate.as_of}"
        expected_body_content = [
            f"SGDUSD rate for {latest_rate.as_of} = {latest_rate.rate:.4f}",
            f"(4.17% from {previous_rate.as_of})",
        ]

        mock_email_service_class.assert_called_once()
        call_args = mock_email_service_class.call_args[1]
        assert call_args["recipient"] == "admin@example.com"
        assert call_args["subject"] == expected_subject
        assert all(content in call_args["body"] for content in expected_body_content)

        mock_email_service.send_async.assert_called_once()


@pytest.mark.asyncio
async def test_send_exchange_rate_refresh_email_no_admin_email():
    mock_exchange_rate_service = AsyncMock(spec=ExchangeRateServiceInterface)

    with (
        patch("app.tasks.notifications.email_settings") as mock_email_settings,
        patch("app.tasks.notifications.EmailService") as mock_email_service_class,
        patch("app.tasks.notifications.logger") as mock_logger,
    ):
        mock_email_settings.admin_email = None

        await send_exchange_rate_refresh_email(exchange_rate_service=mock_exchange_rate_service)

        mock_exchange_rate_service.get_historical_rates.assert_not_called()
        mock_email_service_class.assert_not_called()
        mock_logger.warning.assert_called_once_with("No admin email found")


@pytest.mark.asyncio
async def test_send_exchange_rate_refresh_email_not_enough_rates():
    mock_exchange_rate_service = AsyncMock(spec=ExchangeRateServiceInterface)

    latest_rate = build_exchange_rate(
        as_of=date(2024, 5, 2), base_currency_code="SGD", quote_currency_code="USD", rate=Decimal("0.75")
    )
    mock_exchange_rate_service.get_historical_rates.return_value = [latest_rate]

    with (
        patch("app.tasks.notifications.email_settings") as mock_email_settings,
        patch("app.tasks.notifications.EmailService") as mock_email_service_class,
        patch("app.tasks.notifications.logger") as mock_logger,
    ):
        mock_email_settings.admin_email = "admin@example.com"

        await send_exchange_rate_refresh_email(exchange_rate_service=mock_exchange_rate_service)

        mock_exchange_rate_service.get_historical_rates.assert_called_once()
        mock_email_service_class.assert_not_called()
        mock_logger.warning.assert_called_once_with("Not enough exchange rates found")


@pytest.mark.asyncio
async def test_send_exchange_rate_refresh_email_empty_rates():
    mock_exchange_rate_service = AsyncMock(spec=ExchangeRateServiceInterface)

    mock_exchange_rate_service.get_historical_rates.return_value = []

    with (
        patch("app.tasks.notifications.email_settings") as mock_email_settings,
        patch("app.tasks.notifications.EmailService") as mock_email_service_class,
        patch("app.tasks.notifications.logger") as mock_logger,
    ):
        mock_email_settings.admin_email = "admin@example.com"

        await send_exchange_rate_refresh_email(exchange_rate_service=mock_exchange_rate_service)

        mock_exchange_rate_service.get_historical_rates.assert_called_once()
        mock_email_service_class.assert_not_called()
        mock_logger.warning.assert_called_once_with("Not enough exchange rates found")
