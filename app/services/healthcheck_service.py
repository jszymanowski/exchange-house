import httpx

from app.core.config import healthcheck_settings


class HealthcheckService:
    async def ping_heartbeat(self) -> None:
        await self._ping(healthcheck_settings.heartbeat_check_url)

    async def _ping(self, url: str) -> None:
        async with httpx.AsyncClient() as client:
            await client.get(url)


healthcheck_service = HealthcheckService()
