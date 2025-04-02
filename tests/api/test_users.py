import pytest
import requests

BASE_URL = "http://your-k8s-service/api"

@pytest.fixture
def user_payload():
    return {"username": "testuser", "password": "secure123"}

def test_create_user(user_payload):
    response = requests.post(f"{BASE_URL}/users", json=user_payload)
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_users():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)