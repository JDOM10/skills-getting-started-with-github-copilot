
import pytest
from fastapi.testclient import TestClient
from src.app import app
from src.data import activities
import copy

client = TestClient(app)

# Use the test-only endpoint to reset activities state in the app
@pytest.fixture(autouse=True)
def reset_activities():
    client.post("/test/reset-activities")

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.post(f"/activities/{activity}/unregister", params={"email": email})
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response2.status_code == 400
    # Clean up
    client.post(f"/activities/{activity}/unregister", params={"email": email})


