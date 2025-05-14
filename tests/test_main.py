from fastapi.testclient import TestClient
from book_api.main import app

client = TestClient(app)

def test_get_all_books():
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "title" in data[0]

def test_get_books_by_country():
    response = client.get("/books", params={"country": "Brazil"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for book in data:
        assert book["publisher_country"] == "Brazil"

def test_add_book_unauthorized():
    response = client.post("/books", json={
        "title": "The Docker Handbook",
        "price": "12.99",
        "availability": "In stock",
        "product_page": "https://example.com/book",
        "star_rating": 4,
        "publisher_country": "Germany"
    }, headers={"X-API-Key": "invalidkey"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid API Key"}


def test_add_book_authorized():
    response = client.post("/books", json={
        "title": "The Docker Handbook",
        "price": "12.99",
        "availability": "In stock",
        "product_page": "https://example.com/book",
        "star_rating": 4,
        "publisher_country": "Germany"
    }, headers={"X-API-Key": "supersecretkey"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "The Docker Handbook"

def test_delete_book_authorized():
    title = "The Docker Handbook"
    response = client.delete(f"/books/{title}", headers={"X-API-Key": "supersecretkey"})
    assert response.status_code in [200, 404]  # 404 nếu book đã bị xóa rồi
