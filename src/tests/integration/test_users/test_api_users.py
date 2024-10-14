# TODO: Реализовать тесты на API пользователей
from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import app

client = TestClient(app)


async def test_auth(client: AsyncClient, admin_token: str):
    resp = await client.get("/users/")
    assert resp.status_code == 403
    request = {
        "login": "test",
        "name": "test",
        "email": "test@example.com",
        "password": "test",
    }
    resp = await client.post(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=request,
    )
    assert resp.status_code == 201
    resp = await client.post(
        "/auth", json={"login": "test", "password": "test"}
    )
    assert resp.status_code == 200


async def test_user_list(client: AsyncClient, admin_token: str):
    """Check authorisation requirement and getting user list"""
    resp = await client.get("/users/")
    assert resp.status_code == 403

    resp = await client.get(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    assert len(resp.json()) == 1


async def test_user_create(client: AsyncClient, admin_token: str):
    """Testing creating new test user"""
    resp = await client.get("/users/")
    assert resp.status_code == 403
    request = {
        "login": "test",
        "name": "test",
        "email": "test@example.com",
        "password": "test",
    }
    resp = await client.post(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=request,
    )
    assert resp.status_code == 201


async def test_user_me(client: AsyncClient, admin_token: str):
    """Check authorisation requirement and getting user "Me" """
    resp = await client.get("/users/me")
    assert resp.status_code == 403

    resp = await client.get(
        "/users/me", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200


async def test_user_other(client: AsyncClient, admin_token: str):
    """Check authorisation requirement and getting
    other user by his username"""

    resp = await client.get("/users/test")
    assert resp.status_code == 403
    resp = await client.get(
        "/users/test",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 404

    request = {
        "login": "test",
        "name": "test",
        "email": "test@example.com",
        "password": "test",
    }
    resp = await client.post(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=request,
    )
    assert resp.status_code == 201
    resp = await client.get(
        "/users/test", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200
    assert resp.json()["email"] == "test@example.com"
    assert resp.json()["login"] == "test"
    assert resp.json()["name"] == "test"


async def test_user_delete(client: AsyncClient, admin_token: str):
    """Check for deleting test_user"""
    resp = await client.delete("/users/test")
    assert resp.status_code == 403
    resp = await client.get(
        "/users/test",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 404

    request = {
        "login": "test",
        "name": "test",
        "email": "test@example.com",
        "password": "test",
    }
    resp = await client.post(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=request,
    )
    resp = await client.get(
        "/users/test",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200

    resp = await client.post(
        "/auth", json={"login": "test", "password": "test"}
    )
    assert resp.status_code == 200

    test_token = resp.json()["token"]

    resp = await client.delete(
        "/users/test",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    assert resp.status_code == 200

    resp = await client.get(
        "/users/test",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 404


async def test_fake_password(client: AsyncClient, admin_token: str):
    """Trying to register with wrong password"""
    resp = await client.get("/users/")
    assert resp.status_code == 403
    request = {
        "login": "test",
        "name": "test",
        "email": "test@example.com",
        "password": "test",
    }
    resp = await client.post(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=request,
    )
    resp = await client.post(
        "/auth", json={"login": "test", "password": "fake"}
    )
    assert resp.status_code == 401


async def test_fake_token(client: AsyncClient):
    """Fake token test(not jwt)"""
    resp = await client.get("/users/me")
    assert resp.status_code == 403

    resp = await client.get(
        "/users/me",
        headers={"Authorization": "Bearer fake_token"},
    )
    assert resp.status_code == 400


async def test_wrong_token(client: AsyncClient, admin_token: str):
    """Wrong token test. Wrong decoding"""
    resp = await client.get("/users/me")
    assert resp.status_code == 403

    resp = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {admin_token}evg"},
    )
    assert resp.status_code == 400


async def test_same_login_register(client: AsyncClient, admin_token: str):
    """Testing creating new test user"""
    resp = await client.get("/users/")
    assert resp.status_code == 403
    request = {
        "login": "test",
        "name": "test",
        "email": "test@example.com",
        "password": "test",
    }
    resp = await client.post(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=request,
    )
    assert resp.status_code == 201
    request = {
        "login": "test",
        "name": "test2",
        "email": "test2@example.com",
        "password": "test2",
    }
    resp = await client.post(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=request,
    )
    assert resp.status_code == 400
