import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    # ROTA CORRETA: /auth/register
    response = await client.post(
        "/auth/register",
        json={
            "name": "New User",
            "email": "new@example.com",
            "password": "Password123!",  # Senha Forte
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New User"
    assert "id" in data


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    # Primeiro registra
    await client.post(
        "/auth/register",
        json={
            "name": "New User",
            "email": "login@example.com",
            "password": "Password123!",
        },
    )

    # ROTA CORRETA: /auth/login
    response = await client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "Password123!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert "access_token" in data


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={
            "name": "Me User",
            "email": "me@example.com",
            "password": "Password123!",
        },
    )
    login_res = await client.post(
        "/auth/login",
        data={"username": "me@example.com", "password": "Password123!"},
    )
    token = login_res.json()["access_token"]

    response = await client.get(
        "/users/me", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"
