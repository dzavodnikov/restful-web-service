from rest_app.storage.memory import MemoryBookStorage
from rest_app.storage.sqlite import SQLiteBookStorage


def get_storage(storage_type: str = "memory"):
    storage_params = storage_type.split(":")
    if storage_params[0].lower() in ["sqlite", "sqlite3"]:
        if len(storage_params) != 2:
            raise ValueError('SQLite 3 storage require path of the database: "sqlite:<path_to_database>"')
        return SQLiteBookStorage(storage_params[1])

    return MemoryBookStorage()
