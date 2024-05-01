from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from core.core.db import engine
from core.main import app


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
