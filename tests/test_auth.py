def test_register_user(client):
    response = client.post("/register", json={"email": "user@example.com", "password": "secret"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user@example.com"


def test_login_for_access_token(client):
    client.post("/register", json={"email": "user@example.com", "password": "secret"})

    response = client.post("/token", data={"username": "user@example.com", "password": "secret"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
