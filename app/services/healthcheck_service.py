import httpx

from app.core.config import healthcheck_settings
from app.core.logger import logger


class NoURLSetError(Exception):
    pass


class HealthchecksService:
    def ping_heartbeat(self) -> None:
        self._ping(healthcheck_settings.heartbeat_check_url)

    def ping_refresh_completed(self) -> None:
        self._ping(healthcheck_settings.refresh_completed_url)

    def _ping(self, url: str | None = None, timeout: float = 10.0) -> None:
        if url is None:
            raise NoURLSetError

        with httpx.Client() as client:
            try:
                response = client.get(url, timeout=timeout)
                response.raise_for_status()
                logger.info(f"Successfully pinged {url}")
            except Exception as e:
                logger.error(f"Failed to ping {url}: {str(e)}")
                raise


healthchecks_service = HealthchecksService()
