import pytest
from fastapi.testclient import TestClient
from src.app.main import app
from src.app.services.authServices import limiter
import random
import string

# --- Helper Function ---
def random_string(length=10):
    """Generate a random string for unique usernames/emails."""
    return ''.join(random.choices(string.ascii_letters, k=length))


@pytest.fixture(autouse=True)
def clear_rate_limiter_state():
    """Reset shared rate-limit buckets so tests don't interfere with each other."""
    storage = getattr(limiter, "_storage", None)
    if storage and hasattr(storage, "reset"):
        storage.reset()
    yield
    storage = getattr(limiter, "_storage", None)
    if storage and hasattr(storage, "reset"):
        storage.reset()

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
    assert login_res.status_code == 200, login_res.text
    data = login_res.json()
    return username, data["access_token"], data["refresh_token"]

# --- Integration Tests ---

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


def test_register_duplicate_email():
    """Test that registering the same email twice fails."""
    with TestClient(app) as client:
        email = f"{random_string()}@example.com"
        password = "MyPassword1!"

        client.post("/auth/register", json={
            "username": f"user_{random_string()}",
            "password": password,
            "email": email,
        })

        response = client.post("/auth/register", json={
            "username": f"user_{random_string()}",
            "password": password,
            "email": email,
        })

        assert response.status_code == 400
        assert response.json()["detail"] == "Email already in use"


def test_register_invalid_email_format():
    """Test that invalid email format is rejected by schema validation."""
    with TestClient(app) as client:
        response = client.post("/auth/register", json={
            "username": f"user_{random_string()}",
            "password": "MyPassword1!",
            "email": "not-an-email",
        })

        assert response.status_code == 422


def test_register_missing_required_fields():
    """Test that missing required register fields returns 422."""
    with TestClient(app) as client:
        response = client.post("/auth/register", json={
            "email": f"{random_string()}@example.com"
        })

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


def test_login_nonexistent_user():
    """Test that logging in with an unknown username returns 401."""
    with TestClient(app) as client:
        response = client.post("/auth/login", data={
            "username": f"missing_{random_string()}",
            "password": "WrongPassword1!"
        })

        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect username or password"


def test_login_missing_form_fields():
    """Test that missing OAuth form fields returns 422."""
    with TestClient(app) as client:
        response = client.post("/auth/login", data={"username": "only_username"})

        assert response.status_code == 422


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

def test_rate_limit():
    """Test that rate limiting works on the login endpoint."""
    with TestClient(app) as client:
        username = f"user_{random_string()}"
        password = "MyPassword1!"
        
        # Register the user
        client.post("/auth/register", json={
            "username": username, 
            "password": password,
            "email": f"{username}@example.com"
        })
        
        # Keep trying until the limiter trips. This avoids coupling with prior tests
        # that may have already used part of the shared 10/minute budget.
        hit_limit = False
        for _ in range(20):
            response = client.post("/auth/login", data={
                "username": username,
                "password": "WrongPassword1!"
            })

            if response.status_code == 429:
                hit_limit = True
                break

            assert response.status_code == 401

        assert hit_limit is True
        # precise error message depends on slowapi default or custom config
        assert "Too Many Requests" in response.text or "Rate limit exceeded" in response.text

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


@pytest.mark.xfail(reason="/auth/reset-password endpoint is not implemented yet")
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
