from typing import Dict

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def book_list():
    response = client.get("/book/list")

    assert response.status_code == 200

    return response.json()


def test_book_list_empty():
    assert book_list() == []


def test_book_add():
    book = {
        "author": "John Doe",
        "title": "Awesome Novel",
        "published_date": "1980-02-15"
    }
    response = client.post("/book", json=book)

    assert response.status_code == 200

    persist_book = response.json()
    for key in book:
        assert book[key] == persist_book[key]
    assert int(response.json()["id"]) > 0


def create_book() -> Dict:
    book = {
        "author": "John Doe",
        "title": "Awesome Novel",
        "published_date": "1980-02-15"
    }
    response = client.post("/book", json=book)

    assert response.status_code == 200

    return response.json()


def test_book_list_non_empty():
    existing_book_list = book_list()  # Previous tests can modify storage.

    existing_book_list.append(create_book())
    assert book_list() == existing_book_list

    existing_book_list.append(create_book())
    assert book_list() == existing_book_list  # New books have proper order.

    existing_book_list.append(create_book())
    assert book_list() == existing_book_list


def test_book_update():
    book = create_book()

    update = {
        "title": "Awesome Novel #2"
    }
    response = client.put(f"/book/{book['id']}", json=update)

    assert response.status_code == 200

    persist_book = response.json()
    assert persist_book["title"] == update["title"]


def test_book_delete():
    book = create_book()
    assert book in book_list()

    response = client.delete(f"/book/{book['id']}")

    assert response.status_code == 200

    assert not (book in book_list())
