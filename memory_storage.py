from typing import List

from fastapi import HTTPException

from domain import Book, BookUpdate


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
