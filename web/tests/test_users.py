"""v1 users endpoint tests."""

USER_PAYLOAD = {
    "username": "rexfan",
    "email": "rex@example.com",
    "favorite_dino": "Tyrannosaurus",
    "first_name": "Rex",
    "last_name": "Fan",
    "middle_initial": "T",
}


def test_create_user_returns_201(client):
    r = client.post("/api/v1/users", json=USER_PAYLOAD)
    assert r.status_code == 201
    body = r.json()
    assert body["username"] == "rexfan"
    assert body["email"] == "rex@example.com"
    assert body["full_name"] == "Fan, Rex T"
    assert "id" in body


def test_list_users(client):
    client.post("/api/v1/users", json=USER_PAYLOAD)
    r = client.get("/api/v1/users")
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["username"] == "rexfan"


def test_filter_users_by_username(client):
    client.post("/api/v1/users", json=USER_PAYLOAD)
    r = client.get("/api/v1/users", params={"username": "rexfan"})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["full_name"] == "Fan, Rex T"


def test_filter_users_by_username_missing_returns_404(client):
    r = client.get("/api/v1/users", params={"username": "nobody"})
    assert r.status_code == 404


def test_get_user_by_id(client):
    created = client.post("/api/v1/users", json=USER_PAYLOAD).json()
    user_id = created["id"]
    r = client.get(f"/api/v1/users/{user_id}")
    assert r.status_code == 200
    assert r.json()["id"] == user_id


def test_get_user_by_id_missing_returns_404(client):
    r = client.get("/api/v1/users/9999")
    assert r.status_code == 404
    assert "detail" in r.json()


def test_delete_user_returns_204(client):
    created = client.post("/api/v1/users", json=USER_PAYLOAD).json()
    user_id = created["id"]
    r = client.delete(f"/api/v1/users/{user_id}")
    assert r.status_code == 204
    # Second delete -> 404
    r2 = client.delete(f"/api/v1/users/{user_id}")
    assert r2.status_code == 404


def test_invalid_email_returns_422(client):
    bad = dict(USER_PAYLOAD)
    bad["email"] = "not-an-email"
    r = client.post("/api/v1/users", json=bad)
    assert r.status_code == 422
