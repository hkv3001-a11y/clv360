import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def client(tmp_path, monkeypatch):
    import database
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    database.init_db()
    from fastapi.testclient import TestClient
    from main import app
    with TestClient(app) as c:
        yield c
