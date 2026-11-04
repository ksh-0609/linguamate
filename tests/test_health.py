"""Tests for the /health endpoint."""

from fastapi.testclient import TestClient

from linguamate import __version__
from linguamate.api.main import create_app
from linguamate.core.config import Settings, get_settings


def _client() -> TestClient:
    """Create a test client whose settings ignore the real .env file."""
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: Settings(
        app_name="TestApp", environment="testing", _env_file=None
    )
    return TestClient(app)


def test_health_returns_ok() -> None:
    response = _client().get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "app_name": "TestApp",
        "version": __version__,
        "environment": "testing",
    }


def test_unknown_route_returns_404() -> None:
    response = _client().get("/this-route-does-not-exist")

    assert response.status_code == 404