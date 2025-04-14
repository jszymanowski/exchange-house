import pytest
from pytest_httpx import HTTPXMock

from app.integrations.healthchecks import HealthchecksClient


@pytest.fixture
def api_client() -> HealthchecksClient:
    return HealthchecksClient()


@pytest.mark.asyncio
class TestHealthchecksClient:
    async def test_ping(self, api_client: HealthchecksClient, httpx_mock: HTTPXMock) -> None:
        url = "http://healthchecks.home/ping/some-id"

        httpx_mock.add_response(
            method="GET",
            url=url,
            text="OK",
            status_code=200,
        )

        await api_client.ping(url)

        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].url == url

    async def test_ping_failure_not_found(self, api_client: HealthchecksClient, httpx_mock: HTTPXMock) -> None:
        url = "http://healthchecks.home/ping/some-id"

        httpx_mock.add_response(
            method="GET",
            url=url,
            status_code=404,
        )

        with pytest.raises(
            ValueError,
            match="Heartbeat check-in failed: 404",
        ):
            await api_client.ping(url)

    async def test_ping_invalid_url(self, api_client: HealthchecksClient) -> None:
        url = "http://example.com/ping/some-id"

        with pytest.raises(
            ValueError,
            match="Invalid healthcheck URL: http://example.com/ping/some-id. Must start with http://healthchecks.home/ping",
        ):
            await api_client.ping(url)
