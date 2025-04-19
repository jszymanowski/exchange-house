from unittest.mock import MagicMock, patch

from app.services.healthchecks_service import NoURLSetError
from app.tasks.heartbeat_task import heartbeat_task


@patch("app.tasks.heartbeat_task.healthchecks_service")
async def test_heartbeat_task_success(mock_healthchecks_service: MagicMock):
    result = heartbeat_task()
    assert result == {"message": None, "status": "SUCCESS"}

    mock_healthchecks_service.ping_heartbeat.assert_called_once()


@patch("app.tasks.heartbeat_task.healthchecks_service")
async def test_heartbeat_task_skipped(mock_healthchecks_service: MagicMock):
    mock_healthchecks_service.ping_heartbeat.side_effect = NoURLSetError

    result = heartbeat_task()
    assert result == {"message": "Heartbeat completed, but no check-in URL set", "status": "SKIPPED"}


@patch("app.tasks.heartbeat_task.healthchecks_service")
async def test_heartbeat_task_failure(mock_healthchecks_service: MagicMock):
    mock_healthchecks_service.ping_heartbeat.side_effect = Exception("Test error")

    result = heartbeat_task()
    assert result == {"message": "Heartbeat completed, but check-in failed: Test error", "status": "FAILURE"}
