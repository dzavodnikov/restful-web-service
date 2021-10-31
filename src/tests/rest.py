from typing import Dict, List, Optional

from fastapi.testclient import TestClient
from requests import Response

from rest_app.rest import app


client = TestClient(app)


def book_list(args: Optional[Dict] = None):
    path = "/book/list"
    if args is not None:
        import urllib.parse
        path += "?" + urllib.parse.urlencode(args)
    response = client.get(path)

    assert response.status_code == 200

    return response.json()


def create_book(book_dict: Dict) -> Dict:
    response = client.post("/book", json=book_dict)

    assert response.status_code == 200

    return response.json()


def test_book_add():
    book = {
        "author": "John Doe",
        "title": "Awesome Novel",
        "published_date": "1980-02-15"
    }

    persist_book = create_book(book)

    for key in book:
        assert book[key] == persist_book[key]
    assert int(persist_book["id"]) > 0


def create_test_book() -> Dict:
    return create_book({
        "author": "John Doe",
        "title": "Awesome Novel",
        "published_date": "1980-02-15"
    })


def test_book_list_non_empty():
    existing_book_list = book_list()  # Previous tests can modify storage.

    existing_book_list.append(create_test_book())
    assert book_list() == existing_book_list

    existing_book_list.append(create_test_book())
    assert book_list() == existing_book_list  # New books have proper order.

    existing_book_list.append(create_test_book())
    assert book_list() == existing_book_list


def delete_all_books() -> None:
    for book in book_list():
        response = client.delete(f"/book/{book['id']}")

        assert response.status_code == 200

    assert book_list() == []


def create_test_book_list() -> List[Dict]:
    book_lst = [
        {
            "author": "John Doe",
            "title": "Awesome Novel",
            "published_date": "1980-02-15"
        },
        {
            "author": "John Doe",
            "title": "Tricky Story",
            "published_date": "1981-04-20"
        },
        {
            "author": "Jack Daniel",
            "title": "Awesome Story",
            "published_date": "1982-06-25"
        }
    ]
    return [create_book(book) for book in book_lst]


def test_book_list_filtering_author():
    delete_all_books()
    create_test_book_list()

    assert len(book_list()) == 3

    assert len(book_list({"author": "John Doe"})) == 2
    assert len(book_list({"author": "Jack Daniel"})) == 1


def test_book_list_filtering_title():
    delete_all_books()
    create_test_book_list()

    assert len(book_list()) == 3

    assert len(book_list({"title": "Awesome*"})) == 2
    assert len(book_list({"title": "*Story"})) == 2
    assert len(book_list({"title": "Tricky*"})) == 1


def test_book_list_filtering_published_date():
    delete_all_books()
    create_test_book_list()

    assert len(book_list()) == 3

    assert len(book_list({"published_date_from": "1980-01-01"})) == 3
    assert len(book_list({"published_date_to": "1983-01-01"})) == 3

    assert len(book_list({"published_date_from": "1980-06-15"})) == 2
    assert len(book_list({"published_date_to": "1982-06-15"})) == 2

    assert len(book_list({"published_date_from": "1980-06-15", "published_date_to": "1982-06-15"})) == 1


def test_book_update():
    book = create_test_book()

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
    book = create_test_book()
    assert book in book_list()

    response = client.delete(f"/book/{book['id']}")

    assert response.status_code == 200

    assert not (book in book_list())


def test_book_delete_not_found():
    non_exists_book_id = get_none_existing_book_id()

    response = client.delete(f"/book/{non_exists_book_id}")

    check_not_found_response(response, non_exists_book_id)
