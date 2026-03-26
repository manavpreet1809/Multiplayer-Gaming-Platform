from fastapi.testclient import TestClient
from app.main import app
import random
import string

# --- Helper Functions ---
def random_string(length=10):
    """Generate a random string for unique usernames/emails."""
    return ''.join(random.choices(string.ascii_letters, k=length))


def register_and_login(client):
    """Register a fresh user and log in, returning (username, access_token, refresh_token)."""
    username = f"user_{random_string()}"
    password = "MyPassword1!"
    client.post("/auth/register", json={
        "username": username,
        "password": password,
        "email": f"{username}@example.com",
    })
    login_res = client.post("/auth/login", data={
        "username": username,
        "password": password,
    })
    data = login_res.json()
    return username, data["access_token"], data["refresh_token"]

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

        assert response.status_code == 422
        detail = response.json()["detail"]
        assert any("password" in str(e).lower() for e in detail)


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
        username, access_token, _ = register_and_login(client)

        response = client.get("/auth/me", headers={
            "Authorization": f"Bearer {access_token}"
        })

        assert response.status_code == 200
        assert response.json()["username"] == username


def test_refresh_token():
    """Test exchanging a refresh token for a new token pair."""
    with TestClient(app) as client:
        _, _, refresh_token = register_and_login(client)

        response = client.post("/auth/refresh", json={
            "refresh_token": refresh_token
        })

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["refresh_token"] != refresh_token


def test_refresh_revokes_old_token():
    """Test that a used refresh token cannot be replayed."""
    with TestClient(app) as client:
        _, _, refresh_token = register_and_login(client)

        # First refresh succeeds
        client.post("/auth/refresh", json={"refresh_token": refresh_token})

        # Same token should now be revoked
        response = client.post("/auth/refresh", json={"refresh_token": refresh_token})
        assert response.status_code == 401


def test_logout():
    """Test that logout revokes tokens and blocks subsequent /me calls."""
    with TestClient(app) as client:
        _, access_token, refresh_token = register_and_login(client)

        response = client.post("/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"refresh_token": refresh_token},
        )
        assert response.status_code == 204

        # Access token should now be revoked
        me_res = client.get("/auth/me", headers={
            "Authorization": f"Bearer {access_token}"
        })
        assert me_res.status_code == 401


def test_reset_password():
    """Test resetting a user's password and logging in with the new one."""
    with TestClient(app) as client:
        username, _, _ = register_and_login(client)
        new_password = "NewPassword2@"

        response = client.post("/auth/reset-password", json={
            "identifier": username,
            "new_password": new_password,
        })
        assert response.status_code == 200

        # Old password should fail
        old_login = client.post("/auth/login", data={
            "username": username, "password": "MyPassword1!"
        })
        assert old_login.status_code == 401

        # New password should work
        new_login = client.post("/auth/login", data={
            "username": username, "password": new_password
        })
        assert new_login.status_code == 200
        assert "access_token" in new_login.json()
