import httpx


class HealthchecksClient:
    TIMEOUT_SECONDS = 10.0
    REQUIRED_PREFIX = "http://healthchecks.home/ping"

    def validate_url(self, url: str) -> bool:
        """Validate that the URL begins with the required healthchecks prefix."""
        return url.startswith(self.REQUIRED_PREFIX)

    async def ping(self, url: str) -> None:
        if not self.validate_url(url):
            raise ValueError(f"Invalid healthcheck URL: {url}. Must start with {self.REQUIRED_PREFIX}")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=self.TIMEOUT_SECONDS)

                if response.status_code >= 400:
                    raise ValueError(f"Heartbeat check-in failed: {response.status_code}")
        except httpx.HTTPError as e:
            raise ValueError(f"Heartbeat check-in failed: {str(e)}") from e


def get_healthchecks_client() -> HealthchecksClient:
    return HealthchecksClient()
