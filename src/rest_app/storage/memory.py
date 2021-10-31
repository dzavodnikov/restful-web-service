from typing import List, Optional

from rest_app.domain import Book, BookUpdate, BookNotFoundException


class MemoryBookStorage:
    """Base storage for books that save data in memory."""

    def __init__(self):
        self.id_counter = 0
        self.books = []

    def list(self,
             author: Optional[str],
             title: Optional[str],
             published_date_from: Optional[str],
             published_date_to: Optional[str]) -> List[Book]:
        """Provide list of saved books."""

        return sorted(self.books, key=lambda book: book.id)

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

    def remove(self, book: Book) -> None:
        """Remove book from the storage."""

        self.books.remove(book)

    def persist(self, _book: Book) -> None:
        """Update book in a storage."""

        pass
