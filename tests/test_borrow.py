def test_borrow_book(authenticated_client):
    book_response = authenticated_client.post("/books/", json={
        "title": "Гарри Поттер",
        "author": "Джоан Роулинг",
        "quantity": 1
    })
    book_id = book_response.json()["id"]

    reader_response = authenticated_client.post("/readers/", json={"name": "Петя", "email": "123petya123@example.com"})
    reader_id = reader_response.json()["id"]

    borrow_response = authenticated_client.post("/borrowed/borrow", json={"book_id": book_id, "reader_id": reader_id})
    assert borrow_response.status_code == 200

    book_data = authenticated_client.get(f"/books/{book_id}").json()
    assert book_data["quantity"] == 0


def test_cannot_borrow_more_than_3_books(authenticated_client):
    book_ids = []
    for i in range(3):
        response = authenticated_client.post("/books/", json={"title": f"Книга {i+1}", "author": "Автор", "quantity": 1})
        assert response.status_code == 200
        book_ids.append(response.json()["id"])

    reader_response = authenticated_client.post("/readers/", json={"name": "Петя", "email": "petya@example.com"})
    assert reader_response.status_code == 200
    reader_id = reader_response.json()["id"]

    for book_id in book_ids:
        response = authenticated_client.post("/borrowed/borrow", json={"book_id": book_id, "reader_id": reader_id})
        assert response.status_code == 200

    fourth_book = authenticated_client.post("/books/", json={"title": "4-я книга", "author": "Автор", "quantity": 1})
    fourth_book_id = fourth_book.json()["id"]

    response = authenticated_client.post("/borrowed/borrow", json={"book_id": fourth_book_id, "reader_id": reader_id})

    assert response.status_code == 400
    assert "читатель уже взял 3 книги" in response.json()["detail"].lower()