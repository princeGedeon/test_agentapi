import os

import pytest
from fastapi.testclient import TestClient

from core.database.init import init_db
from core.main import app



TEST_DB_PATH = "./data/flight_test.db"


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    original_db_path = os.environ.get("DATABASE_PATH")
    #  BD pour les tests
    os.environ["DATABASE_PATH"] = TEST_DB_PATH
    # Supprime si elle existait déjà
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    # Initaliser
    init_db()

    #  A la fin
    yield

    # test to prod
    if original_db_path is not None:
        os.environ["DATABASE_PATH"] = original_db_path
    else:
        del os.environ["DATABASE_PATH"]

    # supprimer BD test
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

@pytest.fixture
def client():
    return TestClient(app)
