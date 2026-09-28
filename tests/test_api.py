from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.main import app


TEST_TOKEN = "test-secret-token"


def create_client() -> TestClient:
    app.dependency_overrides[get_settings] = lambda: Settings(app_token=TEST_TOKEN)
    return TestClient(app)


def test_returns_needs_for_known_region() -> None:
    with create_client() as client:
        response = client.post(
            "/api/v1/staffing/needs",
            headers={"x-app-token": TEST_TOKEN},
            json={"region": "Москва"},
        )

    assert response.status_code == 200
    assert response.json() == {
        "2025": {"total": 1500, "replacement": 600, "additional": 900},
        "2026": {"total": 1800, "replacement": 700, "additional": 1100},
    }


def test_rejects_missing_token() -> None:
    with create_client() as client:
        response = client.post("/api/v1/staffing/needs", json={"region": "Москва"})

    assert response.status_code == 401


def test_rejects_invalid_token() -> None:
    with create_client() as client:
        response = client.post(
            "/api/v1/staffing/needs",
            headers={"x-app-token": "wrong-token"},
            json={"region": "Москва"},
        )

    assert response.status_code == 401


def test_returns_not_found_for_unknown_region() -> None:
    with create_client() as client:
        response = client.post(
            "/api/v1/staffing/needs",
            headers={"x-app-token": TEST_TOKEN},
            json={"region": "Вымышленный регион"},
        )

    assert response.status_code == 404
    assert "Вымышленный регион" in response.json()["detail"]


def test_rejects_missing_region() -> None:
    with create_client() as client:
        response = client.post(
            "/api/v1/staffing/needs",
            headers={"x-app-token": TEST_TOKEN},
            json={},
        )

    assert response.status_code == 422


def test_rejects_empty_region() -> None:
    with create_client() as client:
        response = client.post(
            "/api/v1/staffing/needs",
            headers={"x-app-token": TEST_TOKEN},
            json={"region": ""},
        )

    assert response.status_code == 422
