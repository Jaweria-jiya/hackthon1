from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession # Import AsyncSession
import uuid
import pytest # Import pytest

# Assuming the app and db_session fixtures are defined in conftest.py
# and automatically discovered by pytest.

@pytest.mark.asyncio
async def test_read_users(client: TestClient):
    client.post("/api/signup", json={"email": "user1@example.com", "password": "password1"})
    client.post("/api/signup", json={"email": "user2@example.com", "password": "password2"})

    response = client.get("/api/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert any(user["email"] == "user1@example.com" for user in data)
    assert any(user["email"] == "user2@example.com" for user in data)

@pytest.mark.asyncio
async def test_read_user(client: TestClient):
    create_response = client.post(
        "/api/signup",
        json={"email": "single@example.com", "password": "password"}
    )
    user_id = create_response.json()["id"]

    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "single@example.com"
    assert data["id"] == user_id

@pytest.mark.asyncio
async def test_read_non_existent_user(client: TestClient):
    non_existent_id = uuid.uuid4()
    response = client.get(f"/api/users/{non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_update_user(client: TestClient):
    create_response = client.post(
        "/api/signup",
        json={"email": "old@example.com", "password": "password"}
    )
    user_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/users/{user_id}",
        json={"email": "new@example.com"} # Note: update does not require password
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["email"] == "new@example.com"
    assert data["id"] == user_id

    # Verify updated user can be read
    get_response = client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == "new@example.com"

@pytest.mark.asyncio
async def test_update_non_existent_user(client: TestClient):
    non_existent_id = uuid.uuid4()
    response = client.put(
        f"/api/users/{non_existent_id}",
        json={"email": "new_email@example.com"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_delete_user(client: TestClient):
    create_response = client.post(
        "/api/signup",
        json={"email": "delete@example.com", "password": "password"}
    )
    user_id = create_response.json()["id"]

    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 204

    # Verify user is deleted
    get_response = client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 404
