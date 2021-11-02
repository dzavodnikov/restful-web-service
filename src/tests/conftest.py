import pytest

from _pytest.fixtures import SubRequest
from fastapi.testclient import TestClient
from types import ModuleType


storages = ["sqlite:data/book_storage.db.test", "memory"]


def update_env_var(name: str, value: str) -> None:
    """Define environment variable."""
    import os
    os.environ[name] = value


def reload_module(module_name: str) -> ModuleType:
    """
    That method load module at first time and reload it after.
    Useful for reinitialize module with different system variables.
    """
    import sys
    import importlib
    if module_name not in sys.modules:
        return importlib.import_module(module_name)
    else:
        module = importlib.import_module(module_name)
        return importlib.reload(module)


@pytest.fixture
def client(request: SubRequest) -> TestClient:
    """Change system variable base of parameter from tests and reload module to reinitialize it."""
    update_env_var("storage_type", request.param)
    module = reload_module("rest_app.rest")
    return TestClient(getattr(module, "app"))
