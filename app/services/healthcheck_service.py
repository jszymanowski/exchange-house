import httpx

from app.core.config import healthcheck_settings
from app.core.logger import logger


class HealthcheckService:
    def ping_heartbeat(self) -> None:
        self._ping(healthcheck_settings.heartbeat_check_url)

    def _ping(self, url: str | None = None, timeout: float = 10.0) -> None:
        if url is None:
            logger.warning("No URL provided for healthcheck, skipping")
            return

        with httpx.Client() as client:
            try:
                response = client.get(url, timeout=timeout)
                response.raise_for_status()
                logger.info(f"Successfully pinged {url}")
            except Exception as e:
                logger.error(f"Failed to ping {url}: {str(e)}")
                raise


healthcheck_service = HealthcheckService()
