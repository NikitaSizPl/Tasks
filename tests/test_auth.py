from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email": "testuser@example.com"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"


def test_login_user():
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


