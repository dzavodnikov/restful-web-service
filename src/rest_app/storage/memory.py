from rest_app.domain import Book, BookUpdate, BookNotFoundException

from typing import List, Optional

from datetime import date
import re


class MemoryBookStorage:
    """Base storage for books that save data in memory."""

    def __init__(self):
        self.id_counter = 0
        self.books = []

    @staticmethod
    def string_compare_expr(key: str, value: str):
        if value is None:
            return None

        reg_exp = re.compile(value.replace("?", ".?").replace("*", ".*"))
        return lambda record: reg_exp.match(getattr(record, key))

    @staticmethod
    def date_compare_expr(key: str, comparator: str, value: date):
        if value is None:
            return None

        if comparator == ">":
            return lambda record: getattr(record, key) > value
        else:
            return lambda record: getattr(record, key) < value

    def list(self,
             author: Optional[str] = None,
             title: Optional[str] = None,
             published_date_from: Optional[date] = None,
             published_date_to: Optional[date] = None) -> List[Book]:
        """Provide list of saved books."""

        filter_conditions = [MemoryBookStorage.string_compare_expr("author", author),
                             MemoryBookStorage.string_compare_expr("title", title),
                             MemoryBookStorage.date_compare_expr("published_date", ">", published_date_from),
                             MemoryBookStorage.date_compare_expr("published_date", "<", published_date_to)]

        result = []
        for record in self.books:
            add = True
            for cond in filter_conditions:
                if not cond:
                    continue
                if cond(record):
                    continue
                add = False
                break
            if add:
                result.append(record)
        return result

    def find(self, book_id: int) -> Book:
        """Find book from the storage. Can be used for modification or delete requests."""

        for book in self.books:
            if book.id == book_id:
                return book
        raise BookNotFoundException(book_id)

    def create(self, book: BookUpdate) -> Book:
        """Create book in a storage. Populate unique identifier for future requests."""

        self.id_counter += 1
        book = Book(id=self.id_counter, **book.dict())  # Join parameters...
        self.books.append(book)
        return book

    def remove(self, book_id: int) -> None:
        """Remove book from the storage."""

        book = self.find(book_id)
        self.books.remove(book)

    def persist(self, _book: Book) -> None:
        """Update book in a storage."""

        pass
