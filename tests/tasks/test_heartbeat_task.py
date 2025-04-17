from unittest.mock import patch

import pytest

from app.tasks.heartbeat_task import heartbeat_task


@pytest.mark.asyncio
async def test_heartbeat_task_success():
    with (
        patch("app.tasks.heartbeat_task.healthcheck_service") as mock_healthcheck_service,
    ):
        result = heartbeat_task()
        assert result == {"message": None, "status": "SUCCESS"}

        mock_healthcheck_service.ping_heartbeat.assert_called_once()


@pytest.mark.asyncio
async def test_heartbeat_task_skipped():
    with (
        patch("app.tasks.heartbeat_task.settings") as mock_settings,
    ):
        mock_settings.heartbeat_check_url = None

        result = heartbeat_task()
        assert result == {"message": "Heartbeat completed, but no check-in URL set", "status": "SKIPPED"}


@pytest.mark.asyncio
async def test_heartbeat_task_failure():
    with (
        patch("app.tasks.heartbeat_task.healthcheck_service") as mock_healthcheck_service,
    ):
        mock_healthcheck_service.ping_heartbeat.side_effect = Exception("Test error")

        result = heartbeat_task()
        assert result == {"message": "Heartbeat completed, but check-in failed: Test error", "status": "FAILURE"}
