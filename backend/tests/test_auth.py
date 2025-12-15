from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession # Import AsyncSession
import pytest

from app.core.config import settings

@pytest.mark.asyncio
async def test_signup(client: TestClient, db_session: AsyncSession):
    response = client.post(
        "/api/signup",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_signup_existing_email(client: TestClient, db_session: AsyncSession):
    client.post(
        "/api/signup",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    response = client.post(
        "/api/signup",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

@pytest.mark.asyncio
async def test_login(client: TestClient, db_session: AsyncSession):
    # First, create a user
    client.post(
        "/api/signup",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    
    response = client.post(
        "/api/login",
        data={"username": "test@example.com", "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_incorrect_password(client: TestClient, db_session: AsyncSession):
    client.post(
        "/api/signup",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    
    response = client.post(
        "/api/login",
        data={"username": "test@example.com", "password": "wrongpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

@pytest.mark.asyncio
async def test_login_non_existent_user(client: TestClient, db_session: AsyncSession):
    response = client.post(
        "/api/login",
        data={"username": "nosuchuser@example.com", "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
