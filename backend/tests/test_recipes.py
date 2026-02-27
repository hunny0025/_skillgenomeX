import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

# Mocking external services would be ideal here, 
# but for basic structure verification we check that endpoints exist.
# Since we don't have a real token in CI/tests, actual calls might 401 or similar,
# but we can check if the route is registered.

def test_recipes_route_exists():
    # Without token, this might fail with 401 or 500 depending on how the service handles it.
    # But it verifies the app structure is correct.
    response = client.get("/api/v1/recipes/info")
    # We expect either 200 (if token works), 401/403 (if token invalid), or 500 (connection error).
    # But definitely NOT 404.
    assert response.status_code != 404
