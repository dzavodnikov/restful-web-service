from typing import Dict

from fastapi.testclient import TestClient
from requests import Response

from main import app


client = TestClient(app)


def book_list():
    response = client.get("/book/list")

    assert response.status_code == 200

    return response.json()


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


def get_none_existing_book_id():
    existing_books = book_list()
    if len(existing_books) == 0:
        return 1
    return max([book["id"] for book in existing_books]) + 1


def check_not_found_response(response: Response, book_id: int):
    assert response.status_code == 404

    assert response.json()["message"] == f"Book with ID {book_id} not found"


def test_book_update_not_found():
    non_exists_book_id = get_none_existing_book_id()

    update = {
        "title": "Awesome Novel"
    }
    response = client.put(f"/book/{non_exists_book_id}", json=update)

    check_not_found_response(response, non_exists_book_id)


def test_book_delete_one():
    book = create_book()
    assert book in book_list()

    response = client.delete(f"/book/{book['id']}")

    assert response.status_code == 200

    assert not (book in book_list())


def test_book_delete_all():
    for book in book_list():
        response = client.delete(f"/book/{book['id']}")

        assert response.status_code == 200

    assert book_list() == []


def test_book_delete_not_found():
    non_exists_book_id = get_none_existing_book_id()

    response = client.delete(f"/book/{non_exists_book_id}")

    check_not_found_response(response, non_exists_book_id)
