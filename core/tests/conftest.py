import pytest
from fastapi.testclient import TestClient

from core.database.init import init_db
from core.main import app


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    init_db() 

@pytest.fixture
def client():
    return TestClient(app)
