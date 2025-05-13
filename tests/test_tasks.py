from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_task():
    login_response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    token = login_response.json()["access_token"]

    response = client.post("/tasks/", json={
        "title": "Test Task",
        "description": "Test description"
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"
    assert response.json()["description"] == "Test description"


def test_get_tasks():
    login_response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    token = login_response.json()["access_token"]

    response = client.get("/tasks/", headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)