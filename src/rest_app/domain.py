from datetime import date
from typing import Optional

from pydantic import BaseModel


class BookNotFoundException(Exception):
    """Book was not found in storage."""

    def __init__(self, book_id: int):
        self.book_id = book_id


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
