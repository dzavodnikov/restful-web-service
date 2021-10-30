from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel

from datetime import date
from typing import List, Optional


class BookUpdate(BaseModel):
    """Class for book create or update requests. Contain data that can came from the user."""
    author: Optional[str]
    title: Optional[str]
    published_date: Optional[date]

    class Config:
        max_anystr_length = 1024
        allow_mutation = False


class Book(BookUpdate):
    """Class for saving books. Contain all data about the book."""
    id: int

    class Config:
        allow_mutation = True


class MemoryBookStorage:
    """Base storage for books that save data in memory."""

    def __init__(self):
        self.id_counter = 0
        self.books = []

    def list(self) -> List[Book]:
        """Provide list of saved books."""
        return sorted(self.books, key=lambda book: book.id)

    def find(self, book_id: int) -> Book:
        """Find book from the storage. Can be used for modification or delete requests."""
        for book in self.books:
            print(f"Search ID {book_id} and compare with {book.id}: {book_id == book.id}")
            if book.id == book_id:
                return book
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

    def create(self, book: BookUpdate) -> Book:
        """Create book in a storage. Populate unique identifier for future requests."""
        self.id_counter += 1
        book = Book(id=self.id_counter, **book.dict())  # Join parameters...
        self.books.append(book)
        return book

    def remove(self, book: Book) -> None:
        """Remove book from the storage."""
        self.books.remove(book)

    def persist(self, _book: BookUpdate) -> None:
        """Update book in a storage."""
        pass


app = FastAPI()
book_storage = MemoryBookStorage()


@app.get("/book/list")
async def book_list() -> List[Book]:
    return book_storage.list()


@app.post("/book")
async def book_add(book: BookUpdate) -> Book:
    persist_book = book_storage.create(book)
    return persist_book


@app.delete("/book/{book_id}")
async def book_delete(book_id: int) -> Book:
    persist_book = book_storage.find(book_id)
    book_storage.remove(persist_book)
    return persist_book


@app.put("/book/{book_id}")
async def book_update(book_id: int, update: BookUpdate) -> Book:
    persist_book = book_storage.find(book_id)

    update_dict = update.dict()
    for field_name in update_dict.keys():
        field_value = update_dict[field_name]  # Extract new value...
        if field_value:  # ...if value is defined...
            setattr(persist_book, field_name, field_value)  # ...update existing object.
    book_storage.persist(persist_book)

    return persist_book


def custom_openapi():
    if app.openapi_schema:  # If was cached...
        return app.openapi_schema  # ...return cache.

    # Create schema at first time...
    openapi_schema = get_openapi(
        title="RESTful Web Service",
        version="1.0.0",
        description="This is a very simple RESTful Web Service",
        routes=app.routes
    )
    app.openapi_schema = openapi_schema  # ...and cache it.
    return app.openapi_schema


app.openapi = custom_openapi
