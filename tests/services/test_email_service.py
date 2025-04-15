import logging
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from pytest import LogCaptureFixture

from app.services.email_service import EmailService


@pytest.fixture
def mock_environment_production() -> Generator[MagicMock]:
    with patch("app.services.email_service.settings") as mock_settings:
        mock_settings.environment = "production"
        yield mock_settings


@pytest.fixture
def mock_email_settings_production() -> Generator[MagicMock]:
    with patch("app.services.email_service.email_settings") as mock_settings:
        mock_settings.is_configured = True
        mock_settings.smtp_server = "smtp.example.com"
        mock_settings.smtp_port = 587
        mock_settings.smtp_username = "test_user"
        mock_settings.smtp_password = "test_password"
        yield mock_settings


@pytest.fixture
def mock_smtp() -> Generator[MagicMock]:
    with patch("app.services.email_service.SMTP", autospec=True) as mock_smtp_class:
        yield mock_smtp_class


@pytest.fixture
def service() -> EmailService:
    return EmailService(
        recipient="test@example.com",
        subject="Test Subject",
        body="Test Body",
    )


def test_send_email_non_production(mock_smtp: MagicMock, caplog: LogCaptureFixture, service: EmailService) -> None:
    caplog.set_level(logging.INFO, logger="app.services.email_service")

    service.send()

    expected_log_msg = "Sending email is disabled in non-production environments."

    assert expected_log_msg in caplog.text

    mock_smtp.assert_not_called()


def test_send_email_production(
    mock_environment_production: MagicMock,
    mock_email_settings_production: MagicMock,
    mock_smtp: MagicMock,
    service: EmailService,
) -> None:
    mock_smtp_instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_smtp_instance

    service.send()

    mock_smtp.assert_called_once_with("smtp.example.com", 587)

    mock_smtp_instance.starttls.assert_called_once()
    mock_smtp_instance.login.assert_called_once_with("test_user", "test_password")

    mock_smtp_instance.sendmail.assert_called_once_with(
        "test_user",
        "test@example.com",
        "Subject: Test Subject\n\nTest Body",
    )
