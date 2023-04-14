from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_token():
    response = client.post("/token/", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_invalid_token():
    response = client.post("/token/", data={"username": "invaliduser", "password": "invalidpass"})
    assert response.status_code == 401
    assert "detail" in response.json()
    assert response.json()["detail"] == "Incorrect username or password"

# testing user

def test_read_users():
    response = client.get("/api/user/get")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user():
    user = {"username": "testuser", "password": "testpass"}
    response = client.post("/api/user/post", json=user)
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"

def test_delete_user():
    # First, create a new user
    user = {"username": "testuser2", "password": "testpass"}
    response = client.post("/api/user/post", json=user)
    assert response.status_code == 201

    # Get the id of the created user
    user_id = response.json()["user_id"]

    # Then, delete the user by id
    response = client.delete(f"/api/user/delete/{user_id}")
    assert response.status_code == 202
    assert response.json()["message"] == "User deleted"

def test_get_user_by_username():
    # First, create a new user
    user = {"username": "testuser3", "password": "testpass"}
    response = client.post("/api/user/post", json=user)
    assert response.status_code == 201

    # Then, get the user by username
    response = client.get("/api/user/get/testuser3")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser3"

def test_update_user():
    # First, create a new user
    user = {"username": "testuser4", "password": "testpass"}
    response = client.post("/api/user/post", json=user)
    assert response.status_code == 201

    # Get the id of the created user
    user_id = response.json()["user_id"]

    # Then, update the user by id
    user = {"username": "testuser5", "password": "testpass2"}
    response = client.put(f"/api/user/put/{user_id}", json=user)
    assert response.status_code == 200
    assert response.json()["message"] == f"User {user_id} updated successfully"
