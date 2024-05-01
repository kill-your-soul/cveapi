from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlmodel import Session

from core.core.config import settings


def test_get_cwes(
    client: TestClient,
    db: Session,
):
    response = client.get("/?page=1&per_page=10")
    assert response.status_code == HTTPStatus.OK
    content = response.json()
    assert len(content["cwes"]) <= 10
    assert "count" in content


def test_read_cwe_by_id(
    client: TestClient,
    db: Session,
):
    cwe_id = "example_id"
    response = client.get(f"/{cwe_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == cwe_id


def test_read_cwe_not_found(
    client: TestClient,
    db: Session,
):
    response = client.get("/non_existing_id")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_cwe(
    client: TestClient,
    db: Session,
):
    cwe_data = {"name": "New CWE", "description": "New CWE description"}
    response = client.post("/", json=cwe_data)
    assert response.status_code == HTTPStatus.CREATED
    content = response.json()
    assert content["name"] == cwe_data["name"]
    assert content["description"] == cwe_data["description"]


def test_create_duplicate_cwe(
    client: TestClient,
    db: Session,
):
    cwe_data = {"name": "Duplicate CWE", "description": "Duplicate description"}
    client.post("/", json=cwe_data)  # First insert
    response = client.post("/", json=cwe_data)  # Duplicate insert
    assert response.status_code == HTTPStatus.CONFLICT


def test_update_cwe(
    client: TestClient,
    db: Session,
):
    cwe_id = "example_id"
    update_data = {"name": "Updated CWE", "description": "Updated details"}
    response = client.put(f"/{cwe_id}", json=update_data)
    assert response.status_code == HTTPStatus.OK
    content = response.json()
    assert content["name"] == update_data["name"]
    assert content["description"] == update_data["description"]


def test_get_cwe_by_cwe_id(
    client: TestClient,
    db: Session,
):
    cwe_id = "CWE-1234"
    response = client.get(f"/cwe_id/{cwe_id}")
    assert response.status_code == HTTPStatus.OK
    content = response.json()
    assert content["cwe_id"] == cwe_id
