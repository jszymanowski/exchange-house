import httpx

from app.core.config import healthcheck_settings
from app.core.logger import get_logger
from app.integrations.healthchecks import HealthchecksClient, get_healthchecks_client


class NoURLSetError(Exception):
    pass


class HealthchecksServiceError(Exception):
    pass


class HealthchecksService:
    def __init__(self, client: HealthchecksClient | None = None):
        self.client = client or get_healthchecks_client()
        self.logger = get_logger("heartbeat")

    async def ping_heartbeat(self) -> None:
        await self._ping(healthcheck_settings.heartbeat_check_url)

    async def ping_refresh_completed(self) -> None:
        await self._ping(healthcheck_settings.refresh_completed_url)

    async def _ping(self, url: str | None = None) -> None:
        if url is None:
            raise NoURLSetError("No Healthchecks URL provided")

        try:
            await self.client.ping(url)
            self.logger.info("Successfully pinged %s", url)
        except ValueError as e:
            message = f"Failed to ping {url}: {str(e)}"
            self.logger.error(message)
            raise HealthchecksServiceError(message) from e
        except httpx.HTTPError as e:
            message = f"HTTP error while pinging {url}: {str(e)}"
            self.logger.error(message)
            raise HealthchecksServiceError(message) from e
        except Exception as e:
            message = f"Failed to ping {url}: {str(e)}"
            self.logger.error(message)
            raise HealthchecksServiceError(message) from e


get_healthchecks_service = HealthchecksService()
