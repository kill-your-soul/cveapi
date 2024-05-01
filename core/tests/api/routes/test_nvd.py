from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlmodel import Session


def test_read_nvd(
    client: TestClient,
    db: Session,
) -> None:
    nvd_id = "example_id"
    response = client.get(f"/{nvd_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == nvd_id


def test_read_nvd_not_found(
    client: TestClient,
    db: Session,
) -> None:
    response = client.get("/non_existing_id")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_nvd(
    client: TestClient,
    db: Session,
) -> None:
    nvd_data = {"name": "New CVE", "description": "New vulnerability"}
    response = client.post("/", json=nvd_data)
    assert response.status_code == HTTPStatus.CREATED
    content = response.json()
    assert content["name"] == nvd_data["name"]
    assert content["description"] == nvd_data["description"]


def test_create_duplicate_nvd(
    client: TestClient,
    db: Session,
) -> None:
    nvd_data = {"name": "Duplicate CVE", "description": "Duplicate vulnerability"}
    client.post("/", json=nvd_data)  # First insert
    response = client.post("/", json=nvd_data)  # Duplicate insert
    assert response.status_code == HTTPStatus.CONFLICT


def test_update_nvd(
    client: TestClient,
    db: Session,
) -> None:
    nvd_id = "example_id"
    update_data = {"name": "Updated CVE", "description": "Updated details"}
    response = client.put(f"/{nvd_id}", json=update_data)
    assert response.status_code == HTTPStatus.OK
    content = response.json()
    assert content["name"] == update_data["name"]
    assert content["description"] == update_data["description"]


def test_get_nvds(
    client: TestClient,
    db: Session,
) -> None:
    response = client.get("/?page=1&per_page=10")
    assert response.status_code == HTTPStatus.OK
    content = response.json()
    assert len(content["nvds"]) <= 10
    assert "count" in content


def test_get_nvd_by_cve_id(
    client: TestClient,
    db: Session,
) -> None:
    cve_id = "CVE-1234-5678"
    response = client.get(f"/cve_id/{cve_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["cve_id"] == cve_id


def test_get_nvd_by_cve_id_not_found(
    client: TestClient,
    db: Session,
) -> None:
    response = client.get("/cve_id/non_existing_cve")
    assert response.status_code == HTTPStatus.NOT_FOUND
