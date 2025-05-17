from collections.abc import AsyncGenerator
from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient

from dispatch_service.database import engine
from dispatch_service.model import Base
# from dispatch_service.main import app
from fastapi import FastAPI

app = FastAPI()

@pytest.fixture(
    scope="session",
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
    ],
)
def anyio_backend(request):
    return request.param


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, Any]:  # noqa: ARG001
    transport = ASGITransport(
        app=app,
    )
    async with AsyncClient(
        base_url="http://0.0.0.0:8000/api/v1",
        headers={"Content-Type": "application/json"},
        transport=transport,
    ) as test_client:
        yield test_client
