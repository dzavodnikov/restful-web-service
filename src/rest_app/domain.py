from pydantic import BaseModel, validator

from datetime import date, datetime
from typing import Optional


class BookNotFoundException(Exception):
    """Book was not found in storage."""

    def __init__(self, book_id: int):
        self.book_id = book_id


class BookUpdate(BaseModel):
    """Class for book create or update requests. Contain data that can came from the user."""
    author: Optional[str]
    title: Optional[str]
    published_date: Optional[date]

    @staticmethod
    def parse_date_str(date_string: str) -> Optional[date]:
        if not date_string:
            return None

        supported_formats = ["%Y-%m-%d", "%Y-%m", "%Y"]

        date_val = None
        for f in supported_formats:
            try:
                date_val = datetime.strptime(date_string, f).date()
                break
            except ValueError:
                continue

        if not date_val:
            raise ValueError(f"Published date '{date_string}' have incorrect format")
        else:
            return date_val

    @validator("published_date", pre=True)
    def split_str(cls, v):
        if isinstance(v, str):
            return BookUpdate.parse_date_str(v)
        return v

    class Config:
        max_anystr_length = 1024
        allow_mutation = False


class Book(BookUpdate):
    """Class for saving books. Contain all data about the book."""
    id: int

    class Config:
        allow_mutation = True
