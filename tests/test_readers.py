def test_create_reader(authenticated_client):
    response = authenticated_client.post("/readers/", json={"name": "Иван Иванов", "email": "ivan@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Иван Иванов"
    assert data["email"] == "ivan@example.com"


def test_get_reader_by_id(authenticated_client):
    response = authenticated_client.get("/readers/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1