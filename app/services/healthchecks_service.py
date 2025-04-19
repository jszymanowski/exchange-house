from app.core.config import healthcheck_settings
from app.core.logger import logger
from app.integrations.healthchecks import HealthchecksClient, get_healthchecks_client


class NoURLSetError(Exception):
    pass


class HealthchecksService:
    def __init__(self, client: HealthchecksClient | None = None):
        self.client = client or get_healthchecks_client()

    async def ping_heartbeat(self) -> None:
        await self._ping(healthcheck_settings.heartbeat_check_url)

    async def ping_refresh_completed(self) -> None:
        await self._ping(healthcheck_settings.refresh_completed_url)

    async def _ping(self, url: str | None = None) -> None:
        if url is None:
            raise NoURLSetError

        try:
            response = await self.client.ping(url)
            response.raise_for_status()
            logger.info(f"Successfully pinged {url}")
        except Exception as e:
            logger.error(f"Failed to ping {url}: {str(e)}")
            raise


get_healthchecks_service = HealthchecksService()
