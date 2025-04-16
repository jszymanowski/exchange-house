import httpx

from app.core.config import healthcheck_settings


class HealthcheckService:
    def ping_heartbeat(self) -> None:
        self._ping(healthcheck_settings.heartbeat_check_url)

    def _ping(self, url: str) -> None:
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()


healthcheck_service = HealthcheckService()
