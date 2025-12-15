from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession # Import AsyncSession
import uuid
import pytest # Import pytest

# Assuming the app and db_session fixtures are defined in conftest.py
# and automatically discovered by pytest.

@pytest.mark.asyncio
async def test_create_progress(client: TestClient):
    # First, create a user
    user_response = client.post("/api/signup", json={"email": "progress_user@example.com", "password": "password"})
    user_id = user_response.json()["id"]

    response = client.post(
        "/api/progress/",
        json={"user_id": str(user_id), "week_number": 1, "completion_percent": 50}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["week_number"] == 1
    assert data["completion_percent"] == 50
    assert data["user_id"] == user_id
    assert "id" in data

@pytest.mark.asyncio
async def test_create_progress_user_not_found(client: TestClient):
    non_existent_user_id = uuid.uuid4()
    response = client.post(
        "/api/progress/",
        json={"user_id": str(non_existent_user_id), "week_number": 1, "completion_percent": 10}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_read_progress_entries(client: TestClient):
    # Create two users and progress entries
    user1_response = client.post("/api/signup", json={"email": "progress_user1@example.com", "password": "password"})
    user1_id = user1_response.json()["id"]
    client.post("/api/progress/", json={"user_id": str(user1_id), "week_number": 1, "completion_percent": 20})

    user2_response = client.post("/api/signup", json={"email": "progress_user2@example.com", "password": "password"})
    user2_id = user2_response.json()["id"]
    client.post("/api/progress/", json={"user_id": str(user2_id), "week_number": 1, "completion_percent": 70})

    # Read all progress entries
    response = client.get("/api/progress/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2 # May include entries from other tests
    assert any(p["completion_percent"] == 20 for p in data)
    assert any(p["completion_percent"] == 70 for p in data)

    # Read progress for a specific user
    response_user1 = client.get(f"/api/progress/?user_id={user1_id}")
    assert response_user1.status_code == 200
    data_user1 = response_user1.json()
    assert len(data_user1) == 1
    assert data_user1[0]["completion_percent"] == 20

@pytest.mark.asyncio
async def test_read_progress_entry(client: TestClient):
    user_response = client.post("/api/signup", json={"email": "read_progress_user@example.com", "password": "password"})
    user_id = user_response.json()["id"]
    create_response = client.post(
        "/api/progress/",
        json={"user_id": str(user_id), "week_number": 2, "completion_percent": 60}
    )
    progress_id = create_response.json()["id"]

    response = client.get(f"/api/progress/{progress_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["week_number"] == 2
    assert data["completion_percent"] == 60
    assert data["id"] == progress_id

@pytest.mark.asyncio
async def test_read_non_existent_progress_entry(client: TestClient):
    non_existent_id = uuid.uuid4()
    response = client.get(f"/api/progress/{non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Progress entry not found"

@pytest.mark.asyncio
async def test_update_progress(client: TestClient):
    user_response = client.post("/api/signup", json={"email": "update_progress_user@example.com", "password": "password"})
    user_id = user_response.json()["id"]
    create_response = client.post(
        "/api/progress/",
        json={"user_id": str(user_id), "week_number": 3, "completion_percent": 10}
    )
    progress_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/progress/{progress_id}",
        json={"user_id": str(user_id), "week_number": 3, "completion_percent": 90}
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["completion_percent"] == 90
    assert data["id"] == progress_id

    # Verify updated progress can be read
    get_response = client.get(f"/api/progress/{progress_id}")
    assert get_response.status_code == 200
    assert get_response.json()["completion_percent"] == 90

@pytest.mark.asyncio
async def test_update_progress_reassign_user(client: TestClient):
    user1_response = client.post("/api/signup", json={"email": "user_for_prog_reassign1@example.com", "password": "password"})
    user1_id = user1_response.json()["id"]
    user2_response = client.post("/api/signup", json={"email": "user_for_prog_reassign2@example.com", "password": "password"})
    user2_id = user2_response.json()["id"]
    
    create_response = client.post(
        "/api/progress/",
        json={"user_id": str(user1_id), "week_number": 4, "completion_percent": 10}
    )
    progress_id = create_response.json()["id"]
    assert create_response.json()["user_id"] == user1_id

    # Reassign progress to user2
    update_response = client.put(
        f"/api/progress/{progress_id}",
        json={"user_id": str(user2_id), "week_number": 4, "completion_percent": 100}
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["user_id"] == user2_id
    assert data["completion_percent"] == 100

@pytest.mark.asyncio
async def test_update_progress_non_existent_user_reassign(client: TestClient):
    user_response = client.post("/api/signup", json={"email": "user_for_bad_prog_reassign@example.com", "password": "password"})
    user_id = user_response.json()["id"]
    create_response = client.post(
        "/api/progress/",
        json={"user_id": str(user_id), "week_number": 5, "completion_percent": 50}
    )
    progress_id = create_response.json()["id"]
    
    non_existent_user_id = uuid.uuid4()
    update_response = client.put(
        f"/api/progress/{progress_id}",
        json={"user_id": str(non_existent_user_id), "week_number": 5, "completion_percent": 75}
    )
    assert update_response.status_code == 404
    assert update_response.json()["detail"] == "User not found for reassignment"

@pytest.mark.asyncio
async def test_delete_progress(client: TestClient):
    user_response = client.post("/api/signup", json={"email": "delete_progress_user@example.com", "password": "password"})
    user_id = user_response.json()["id"]
    create_response = client.post(
        "/api/progress/",
        json={"user_id": str(user_id), "week_number": 6, "completion_percent": 5}
    )
    progress_id = create_response.json()["id"]

    response = client.delete(f"/api/progress/{progress_id}")
    assert response.status_code == 204

    # Verify progress is deleted
    get_response = client.get(f"/api/progress/{progress_id}")
    assert get_response.status_code == 404
