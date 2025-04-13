import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_api_v1_available_dates(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get("/api/v1/available_dates")
    assert response.status_code == 200
    assert response.json() == [
        "2025-04-01",
        "2025-04-02",
        "2025-04-03",
    ]
