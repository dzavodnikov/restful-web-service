from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from typing import List

from domain import Book, BookUpdate, BookNotFoundException
from memory_storage import MemoryBookStorage


app = FastAPI()
book_storage = MemoryBookStorage()


@app.exception_handler(BookNotFoundException)
async def book_not_found_exception(_request: Request, exc: BookNotFoundException):
    return JSONResponse(status_code=404, content={"message": f"Book with ID {exc.book_id} not found"})


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
