# TODO: Реализовать тесты на API пользователей
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


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
    resp = await client.post("/users/")
    assert resp.status_code == 403
    request = {
        "login": "string",
        "name": "string",
        "email": "user@example.com",
        "password": "string",
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


async def test_user_other(client, admin_token, create_test_user):
    """Check authorisation requirement and getting other user"""
    resp = await client.get("/users/{username}")
    assert resp.status_code == 403

    resp = await client.get(
        "/users/{username}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200


# async def test_user_delete(client, admin_token, username="string" ):
#     '''Check for deleting test_user'''
#     resp = await client.delete("/users/{username}")
#     assert resp.status_code == 403

#     resp = await client.delete(
#         "/users/{username}", headers={"Authorization": f"Bearer {admin_token}"} # noqa: E501
#     )
#     assert resp.status_code == 201
#     assert await test_user_me(client, admin_token, username="string" ) == False # noqa: E501
