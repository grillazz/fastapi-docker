import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def test_check(client: AsyncClient):
    assert 1 == 1


async def test_register_trip(client: AsyncClient):
    response = await client.post(
        "/trips",
        json={
            "user_id": "user_123",
            "start_x": 10,
            "start_y": 20,
            "end_x": 30,
            "end_y": 40,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["status"] == "ASSIGNED"