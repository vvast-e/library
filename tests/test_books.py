def test_get_books_unauthorized(client):
    response = client.get("/books/")
    assert response.status_code == 401
    assert "detail" in response.json()
    assert response.json()["detail"] == "Not authenticated"

def test_create_book(authenticated_client):
    response = authenticated_client.post("/books/", json={
        "title": "Война и мир",
        "author": "Лев Толстой",
        "year": 1869,
        "quantity": 3
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Война и мир"
    assert data["author"] == "Лев Толстой"
    assert data["quantity"] == 3


def test_get_books(authenticated_client):
    response = authenticated_client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0