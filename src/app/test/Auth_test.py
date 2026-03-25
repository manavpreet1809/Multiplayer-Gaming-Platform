import pytest
from fastapi.testclient import TestClient
from src.app.main import app
import random
import string

# --- Helper Function ---
def random_string(length=10):
    """Generate a random string for unique usernames/emails."""
    return ''.join(random.choices(string.ascii_letters, k=length))

# --- Tests ---

def test_register_success():
    """Test that a user can register with valid credentials."""
    with TestClient(app) as client:
        username = f"user_{random_string()}"
        email = f"{username}@example.com"
        password = "MyPassword1!"  # Meets all criteria

        response = client.post("/auth/register", json={
            "username": username,
            "password": password,
            "email": email,
            "full_name": "Test User"
        })

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == username
        assert data["email"] == email
        assert "password" not in data  # Password should never be returned


def test_register_duplicate_username():
    """Test that registering the same username twice fails."""
    with TestClient(app) as client:
        username = f"user_{random_string()}"
        password = "MyPassword1!"

        # First registration
        client.post("/auth/register", json={
            "username": username,
            "password": password,
            "email": f"{username}_1@example.com"
        })

        # Second registration (should fail)
        response = client.post("/auth/register", json={
            "username": username,
            "password": password,
            "email": f"{username}_2@example.com"
        })

        assert response.status_code == 400
        assert response.json()["detail"] == "Username already exists"


def test_register_weak_password():
    """Test that weak passwords are rejected."""
    with TestClient(app) as client:
        response = client.post("/auth/register", json={
            "username": f"user_{random_string()}",
            "password": "weak"  # Too short, no numbers/specials
        })

        # Pydantic validation errors return 422 by default
        assert response.status_code == 422


def test_login_success():
    """Test that a registered user can log in and get tokens."""
    with TestClient(app) as client:
        # 1. Register first
        username = f"user_{random_string()}"
        password = "MyPassword1!"
        client.post("/auth/register", json={
            "username": username,
            "password": password,
            "email": f"{username}@example.com"
        })

        # 2. Login (Remember: OAuth2 uses form-data, not JSON)
        response = client.post("/auth/login", data={
            "username": username,
            "password": password
        })

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"


def test_login_invalid_credentials():
    """Test that wrong password returns 401."""
    with TestClient(app) as client:
        # 1. Register
        username = f"user_{random_string()}"
        password = "MyPassword1!"
        client.post("/auth/register", json={
            "username": username,
            "password": password,
            "email": f"{username}@example.com"
        })

        # 2. Login with wrong password
        response = client.post("/auth/login", data={
            "username": username,
            "password": "WrongPassword1!"
        })

        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect username or password"


def test_protected_route_me():
    """Test accessing a protected route with a valid token."""
    with TestClient(app) as client:
        # 1. Register & Login
        username = f"user_{random_string()}"
        password = "MyPassword1!"
        
        client.post("/auth/register", json={
            "username": username, 
            "password": password,
            "email": f"{username}@example.com"
        })
        
        login_res = client.post("/auth/login", data={"username": username, "password": password})
        access_token = login_res.json()["access_token"]

        # 2. Access /auth/me with the token
        response = client.get("/auth/me", headers={
            "Authorization": f"Bearer {access_token}"
        })

        assert response.status_code == 200
        assert response.json()["username"] == username
