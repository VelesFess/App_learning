# TODO: Реализовать тесты на API пользователей


async def test_user_list(client, admin_token):
    resp = await client.get("/users/")
    assert resp.status_code == 403

    resp = await client.get(
        "/users/", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200
    assert len(resp.json()) == 1
