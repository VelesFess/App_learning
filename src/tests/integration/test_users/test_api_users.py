# TODO: Реализовать тесты на API пользователей
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


async def test_auth(client, admin_token):
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
        "/auth", json={"login": "test", "password": "test"}
    )
    assert resp.status_code == 200


async def test_user_list(client, admin_token):
    """Check authorisation requirement and getting user list"""
    resp = await client.get("/users/")
    assert resp.status_code == 403

    resp = await client.get(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    assert len(resp.json()) == 1


async def test_user_create(client, admin_token):
    """Testing creating new admin user"""
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


async def test_user_me(client, admin_token):
    """Check authorisation requirement and getting user "Me" """
    resp = await client.get("/users/")
    assert resp.status_code == 403

    resp = await client.get(
        "/users/", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200


async def test_user_other(client, admin_token):
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


async def test_user_delete(client, admin_token):
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
    resp = await client.get(
        "/users/test",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 404
