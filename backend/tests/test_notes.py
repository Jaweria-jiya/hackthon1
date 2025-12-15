from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession # Import AsyncSession
import uuid
import pytest # Import pytest

# Assuming the app and db_session fixtures are defined in conftest.py
# and automatically discovered by pytest.

@pytest.mark.asyncio
async def test_create_note(client: TestClient):
    # First, create a user
    user_response = client.post("/api/signup", json={"email": "note_user@example.com", "password": "password"})
    user_id = user_response.json()["id"]

    response = client.post(
        "/api/notes/",
        json={"user_id": str(user_id), "content": "My first note"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "My first note"
    assert data["user_id"] == user_id
    assert "id" in data
    assert "created_at" in data

@pytest.mark.asyncio
async def test_create_note_user_not_found(client: TestClient):
    non_existent_user_id = uuid.uuid4()
    response = client.post(
        "/api/notes/",
        json={"user_id": str(non_existent_user_id), "content": "Note for non-existent user"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_read_notes(client: TestClient):
    # Create two users and notes
    user1_response = client.post("/api/signup", json={"email": "note_user1@example.com", "password": "password"})
    user1_id = user1_response.json()["id"]
    client.post("/api/notes/", json={"user_id": str(user1_id), "content": "Note from user 1"})

    user2_response = client.post("/api/signup", json={"email": "note_user2@example.com", "password": "password"})
    user2_id = user2_response.json()["id"]
    client.post("/api/notes/", json={"user_id": str(user2_id), "content": "Note from user 2"})

    # Read all notes
    response = client.get("/api/notes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2 # May include notes from other tests
    assert any(note["content"] == "Note from user 1" for note in data)
    assert any(note["content"] == "Note from user 2" for note in data)

    # Read notes for a specific user
    response_user1 = client.get(f"/api/notes/?user_id={user1_id}")
    assert response_user1.status_code == 200
    data_user1 = response_user1.json()
    assert len(data_user1) == 1
    assert data_user1[0]["content"] == "Note from user 1"

@pytest.mark.asyncio
async def test_read_note(client: TestClient):
    user_response = client.post("/api/signup", json={"email": "read_note_user@example.com", "password": "password"})
    user_id = user_response.json()["id"]
    create_response = client.post(
        "/api/notes/",
        json={"user_id": str(user_id), "content": "Specific note content"}
    )
    note_id = create_response.json()["id"]

    response = client.get(f"/api/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Specific note content"
    assert data["id"] == note_id

@pytest.mark.asyncio
async def test_read_non_existent_note(client: TestClient):
    non_existent_id = uuid.uuid4()
    response = client.get(f"/api/notes/{non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

@pytest.mark.asyncio
async def test_update_note(client: TestClient):
    user_response = client.post("/api/signup", json={"email": "update_note_user@example.com", "password": "password"})
    user_id = user_response.json()["id"]
    create_response = client.post(
        "/api/notes/",
        json={"user_id": str(user_id), "content": "Old note content"}
    )
    note_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/notes/{note_id}",
        json={"user_id": str(user_id), "content": "New note content"}
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["content"] == "New note content"
    assert data["id"] == note_id

    # Verify updated note can be read
    get_response = client.get(f"/api/notes/{note_id}")
    assert get_response.status_code == 200
    assert get_response.json()["content"] == "New note content"

@pytest.mark.asyncio
async def test_update_note_reassign_user(client: TestClient):
    user1_response = client.post("/api/signup", json={"email": "user_for_reassign1@example.com", "password": "password"})
    user1_id = user1_response.json()["id"]
    user2_response = client.post("/api/signup", json={"email": "user_for_reassign2@example.com", "password": "password"})
    user2_id = user2_response.json()["id"]
    
    create_response = client.post(
        "/api/notes/",
        json={"user_id": str(user1_id), "content": "Note to reassign"}
    )
    note_id = create_response.json()["id"]
    assert create_response.json()["user_id"] == user1_id

    # Reassign note to user2
    update_response = client.put(
        f"/api/notes/{note_id}",
        json={"user_id": str(user2_id), "content": "Note reassigned"}
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["user_id"] == user2_id
    assert data["content"] == "Note reassigned"

@pytest.mark.asyncio
async def test_update_note_non_existent_user_reassign(client: TestClient):
    user_response = client.post("/api/signup", json={"email": "user_for_bad_reassign@example.com", "password": "password"})
    user_id = user_response.json()["id"]
    create_response = client.post(
        "/api/notes/",
        json={"user_id": str(user_id), "content": "Note for bad reassign"}
    )
    note_id = create_response.json()["id"]
    
    non_existent_user_id = uuid.uuid4()
    update_response = client.put(
        f"/api/notes/{note_id}",
        json={"user_id": str(non_existent_user_id), "content": "Attempt bad reassign"}
    )
    assert update_response.status_code == 404
    assert update_response.json()["detail"] == "User not found for reassignment"

@pytest.mark.asyncio
async def test_delete_note(client: TestClient):
    user_response = client.post("/api/signup", json={"email": "delete_note_user@example.com", "password": "password"})
    user_id = user_response.json()["id"]
    create_response = client.post(
        "/api/notes/",
        json={"user_id": str(user_id), "content": "Note to delete"}
    )
    note_id = create_response.json()["id"]

    response = client.delete(f"/api/notes/{note_id}")
    assert response.status_code == 204

    # Verify note is deleted
    get_response = client.get(f"/api/notes/{note_id}")
    assert get_response.status_code == 404
