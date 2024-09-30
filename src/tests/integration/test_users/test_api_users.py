# TODO: Реализовать тесты на API пользователей
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


async def test_user_list(client, admin_token):
    resp = await client.get("/users/")
    assert resp.status_code == 403

    resp = await client.get(
        "/users/", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200
    assert len(resp.json()) == 1


async def test_user_create(client, admin_token):
    resp = await client.post("/users/")
    assert resp.status_code == 403

    resp = await client.get(
        "/users/", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200
