from typing import List, Any

from domain import Book, BookUpdate, BookNotFoundException

import sqlite3


class SQLiteBookStorage:
    """Storage for books that save data in SQLite 3."""

    def __init__(self, storage_name="book_storage.db"):
        self.storage_name = storage_name

        # Create table if it was not exists.
        with sqlite3.connect(self.storage_name) as connection:
            cursor = connection.cursor()
            create_books_table = """
                CREATE TABLE IF NOT EXISTS books (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    author          TEXT,
                    title           TEXT,
                    -- SQLite does not have a storage class set aside for storing dates and/or times. 
                    -- See: https://sqlite.org/datatype3.html
                    published_date  TEXT
                );
            """
            cursor.execute(create_books_table)
            connection.commit()

    @staticmethod
    def get_book_columns(cursor) -> List[str]:
        return [column[0] for column in cursor.description]

    @staticmethod
    def read_book(book_columns: List[str], book_record: List[Any]):
        return Book(**dict(zip(book_columns, book_record)))

    def list(self) -> List[Book]:
        """Provide list of saved books."""

        with sqlite3.connect(self.storage_name) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * from books;")
            book_record_list = cursor.fetchall()
            book_columns = SQLiteBookStorage.get_book_columns(cursor)
            return [SQLiteBookStorage.read_book(book_columns, book_record) for book_record in book_record_list]

    def find(self, book_id: int) -> Book:
        """Find book from the storage. Can be used for modification or delete requests."""

        with sqlite3.connect(self.storage_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * from books WHERE id = {book_id};")
            book_record = cursor.fetchone()
            if book_record is None:
                raise BookNotFoundException(book_id)
            book_columns = SQLiteBookStorage.get_book_columns(cursor)
            return SQLiteBookStorage.read_book(book_columns, book_record)

    def create(self, book: BookUpdate) -> Book:
        """Create book in a storage. Populate unique identifier for future requests."""

        with sqlite3.connect(self.storage_name) as connection:
            cursor = connection.cursor()

            book_dict = book.dict()
            columns = ', '.join(book_dict.keys())
            values = ', '.join([f'"{str(val)}"' for val in book_dict.values()])
            create_book = f"INSERT INTO books({columns}) VALUES ({values});"

            cursor.execute(create_book)
            new_id = cursor.lastrowid
            connection.commit()
        return self.find(new_id)

    def remove(self, book: Book) -> None:
        """Remove book from the storage."""

        with sqlite3.connect(self.storage_name) as connection:
            cursor = connection.cursor()

            cursor.execute(f"DELETE FROM books WHERE id = {book.id};")

            connection.commit()

    def persist(self, book: Book) -> None:
        """Update book in a storage."""

        with sqlite3.connect(self.storage_name) as connection:
            cursor = connection.cursor()

            update_items = []
            for item in book.dict().items():
                if item[0] != 'id' and item[1] is not None:
                    update_items.append(item)
            string_items = [f'"{item[0]}" = "{item[1]}"' for item in update_items]
            update_str = ", ".join(string_items)
            update_book = f"UPDATE books SET {update_str} WHERE id = {book.id};"

            cursor.execute(update_book)
            connection.commit()
