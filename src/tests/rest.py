from fastapi.testclient import TestClient
from requests import Response

from typing import Dict, List, Optional

from tests.conftest import storages
import pytest


def book_list(client: TestClient, args: Optional[Dict] = None):
    path = "/book/list"
    if args:
        import urllib.parse
        path += "?" + urllib.parse.urlencode(args)
    response = client.get(path)

    assert response.status_code == 200

    return response.json()


def create_book(client: TestClient, book_dict: Dict) -> Dict:
    response = client.post("/book", json=book_dict)

    assert response.status_code == 200

    return response.json()


@pytest.mark.parametrize("client", storages, indirect=True)
def test_book_add(client: TestClient):
    book = {
        "author": "John Doe",
        "title": "Awesome Novel",
        "published_date": "1980-02-15"
    }

    persist_book = create_book(client, book)

    for key in book:
        assert book[key] == persist_book[key]
    assert int(persist_book["id"]) > 0


def create_test_book(client: TestClient) -> Dict:
    return create_book(client, {
        "author": "John Doe",
        "title": "Awesome Novel",
        "published_date": "1980-02-15"
    })


@pytest.mark.parametrize("client", storages, indirect=True)
def test_book_list_non_empty(client: TestClient):
    existing_book_list = book_list(client)  # Previous tests can modify storage.
    print(existing_book_list)

    existing_book_list.append(create_test_book(client))
    print(existing_book_list)
    print(book_list(client))
    assert book_list(client) == existing_book_list

    existing_book_list.append(create_test_book(client))
    assert book_list(client) == existing_book_list  # New books have proper order.

    existing_book_list.append(create_test_book(client))
    assert book_list(client) == existing_book_list


def delete_all_books(client: TestClient, ) -> None:
    for book in book_list(client):
        response = client.delete(f"/book/{book['id']}")

        assert response.status_code == 200

    assert book_list(client) == []


def create_test_book_list(client: TestClient) -> List[Dict]:
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
    return [create_book(client, book) for book in book_lst]


@pytest.mark.parametrize("client", storages, indirect=True)
def test_book_list_filtering_author(client: TestClient):
    delete_all_books(client)
    create_test_book_list(client)

    assert len(book_list(client)) == 3

    assert len(book_list(client, {"author": "John Doe"})) == 2
    assert len(book_list(client, {"author": "Jack Daniel"})) == 1


@pytest.mark.parametrize("client", storages, indirect=True)
def test_book_list_filtering_title(client: TestClient):
    delete_all_books(client)
    create_test_book_list(client)

    assert len(book_list(client)) == 3

    assert len(book_list(client, {"title": "Awesome*"})) == 2
    assert len(book_list(client, {"title": "*Story"})) == 2
    assert len(book_list(client, {"title": "Tricky*"})) == 1


@pytest.mark.parametrize("client", storages, indirect=True)
def test_book_list_filtering_published_date(client: TestClient):
    delete_all_books(client)
    create_test_book_list(client)

    assert len(book_list(client)) == 3

    assert len(book_list(client, {"published_date_from": "1980-01-01"})) == 3
    assert len(book_list(client, {"published_date_to": "1983-01-01"})) == 3

    assert len(book_list(client, {"published_date_from": "1980-06-15"})) == 2
    assert len(book_list(client, {"published_date_to": "1982-06-15"})) == 2

    assert len(book_list(client, {"published_date_from": "1980-06-15", "published_date_to": "1982-06-15"})) == 1


@pytest.mark.parametrize("client", storages, indirect=True)
def test_book_update(client: TestClient):
    book = create_test_book(client)

    update = {
        "title": "Awesome Novel #2"
    }
    response = client.put(f"/book/{book['id']}", json=update)

    assert response.status_code == 200

    persist_book = response.json()
    assert persist_book["title"] == update["title"]


def get_none_existing_book_id(client: TestClient):
    existing_books = book_list(client)
    if len(existing_books) == 0:
        return 1
    return max([book["id"] for book in existing_books]) + 1


def check_not_found_response(response: Response, book_id: int):
    assert response.status_code == 404

    assert response.json()["message"] == f"Book with ID {book_id} not found"


@pytest.mark.parametrize("client", storages, indirect=True)
def test_book_update_not_found(client: TestClient):
    non_exists_book_id = get_none_existing_book_id(client)

    update = {
        "title": "Awesome Novel"
    }
    response = client.put(f"/book/{non_exists_book_id}", json=update)

    check_not_found_response(response, non_exists_book_id)


@pytest.mark.parametrize("client", storages, indirect=True)
def test_book_delete_one(client: TestClient):
    book = create_test_book(client)
    assert book in book_list(client)

    response = client.delete(f"/book/{book['id']}")

    assert response.status_code == 200

    assert not (book in book_list(client))


@pytest.mark.parametrize("client", storages, indirect=True)
def test_book_delete_not_found(client: TestClient):
    non_exists_book_id = get_none_existing_book_id(client)

    response = client.delete(f"/book/{non_exists_book_id}")

    check_not_found_response(response, non_exists_book_id)
