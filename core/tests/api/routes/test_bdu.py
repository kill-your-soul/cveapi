from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlmodel import Session

from core.core.config import settings


def test_get_bdus(
    client: TestClient,
    db: Session,
):
    response = client.get("/?page=1&per_page=10")
    assert response.status_code == HTTPStatus.OK
    content = response.json()
    assert len(content["bdus"]) <= 10
    assert "count" in content


def test_read_bdu_by_id(
    client: TestClient,
    db: Session,
):
    bdu_id = "example_id"
    response = client.get(f"/{bdu_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == bdu_id


def test_read_bdu_by_id_not_found(
    client: TestClient,
    db: Session,
):
    response = client.get("/non_existing_id")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_bdu_by_bdu_id(
    client: TestClient,
    db: Session,
):
    bdu_id = "Bdu1234"
    response = client.get(f"/bdu_id/{bdu_id}")
    assert response.status_code == HTTPStatus.OK
    content = response.json()
    assert content["bdu_id"] == bdu_id
    assert isinstance(content["cves"], list)  # Check if 'cves' is a list as expected


def test_get_bdu_by_bdu_id_not_found(
    client: TestClient,
    db: Session,
):
    response = client.get("/bdu_id/non_existing_bdu_id")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_bdu(
    client: TestClient,
    db: Session,
):
    bdu_data = {"name": "New BDU", "description": "New BDU description"}
    response = client.post("/", json=bdu_data)
    assert response.status_code == HTTPStatus.CREATED
    content = response.json()
    assert content["name"] == bdu_data["name"]
    assert content["description"] == bdu_data["description"]


def test_create_duplicate_bdu(
    client: TestClient,
    db: Session,
):
    bdu_data = {"name": "Duplicate BDU", "description": "Duplicate description"}
    client.post("/", json=bdu_data)  # First insert
    response = client.post("/", json=bdu_data)  # Duplicate insert
    assert response.status_code == HTTPStatus.CONFLICT


def test_update_bdu(
    client: TestClient,
    db: Session,
):
    bdu_id = "example_id"
    update_data = {"name": "Updated BDU", "description": "Updated description"}
    response = client.put(f"/{bdu_id}", json=update_data)
    assert response.status_code == HTTPStatus.OK
    content = response.json()
    assert content["name"] == update_data["name"]
    assert content["description"] == update_data["description"]
