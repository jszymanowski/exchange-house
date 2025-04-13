from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

from app.main import app


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
