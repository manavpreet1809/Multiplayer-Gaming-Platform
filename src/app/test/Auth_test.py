import pytest
import asyncio
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError
from pydantic import ValidationError
from fastapi.testclient import TestClient
from src.app.main import app
from src.app.services.authServices import create_access_token, create_refresh_token
from src.app.schemas.auth import UserCreate, UserInDB
from src.app.services import authServices
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

# --- Unit Tests for schemas/auth.py ---

@pytest.mark.parametrize(
    "password,expected_message",
    [
        ("Aa1!aaa", "at least 8 characters"),
        ("mypassword1!", "at least one uppercase letter"),
        ("MYPASSWORD1!", "at least one lowercase letter"),
        ("MyPassword!", "at least one digit"),
        ("MyPassword1", "at least one special character"),
    ],
)
def test_usercreate_password_rules(password, expected_message):
    """Each password rule violation should raise a schema validation error."""
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            username=f"user_{random_string()}",
            password=password,
            email=f"{random_string()}@example.com",
        )

    assert expected_message in str(exc_info.value)


def test_usercreate_invalid_email_format():
    """Invalid email format should be rejected by EmailStr validation."""
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            username=f"user_{random_string()}",
            password="MyPassword1!",
            email="user@com",
        )

    assert "valid email address" in str(exc_info.value).lower()


# --- Unit Tests for services/authServices.py ---


def test_create_access_token_claims():
    """Access token should include expected claims and expiry."""
    username = f"user_{random_string()}"
    token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=5),
    )

    payload = jwt.decode(
        token,
        authServices.SECRET_KEY,
        algorithms=[authServices.ALGORITHM],
    )

    assert payload["sub"] == username
    assert payload["type"] == "access"
    assert isinstance(payload.get("jti"), str)
    assert payload.get("jti")
    assert "exp" in payload


def test_create_refresh_token_claims():
    """Refresh token should include expected claims and expiry."""
    username = f"user_{random_string()}"
    token = create_refresh_token(data={"sub": username})

    payload = jwt.decode(
        token,
        authServices.SECRET_KEY,
        algorithms=[authServices.ALGORITHM],
    )

    assert payload["sub"] == username
    assert payload["type"] == "refresh"
    assert isinstance(payload.get("jti"), str)
    assert payload.get("jti")
    assert "exp" in payload


def test_revoke_token_duplicate_jti_is_safe(monkeypatch):
    """Re-revoking the same token (duplicate jti) should not raise."""

    class FakeRevokedTokensCollection:
        async def insert_one(self, _doc):
            raise DuplicateKeyError("duplicate key error")

    monkeypatch.setattr(
        authServices,
        "revoked_tokens_collection",
        FakeRevokedTokensCollection(),
    )

    token = create_access_token(data={"sub": f"user_{random_string()}"})
    # Should not raise DuplicateKeyError
    asyncio.run(authServices.revoke_token(token))


@pytest.mark.parametrize("payload", [{"jti": "abc123", "type": "refresh"}, {"sub": "alice", "type": "refresh"}])
def test_decode_refresh_token_rejects_missing_sub_or_jti(monkeypatch, payload):
    """decode_refresh_token should reject refresh tokens missing sub or jti."""

    def fake_decode(_token, _secret, algorithms):
        return payload

    monkeypatch.setattr(authServices.jwt, "decode", fake_decode)

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(authServices.decode_refresh_token("any-token"))

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid or expired refresh token"


def test_authenticate_user_nonexistent_runs_dummy_hash(monkeypatch):
    """Non-existent user path should verify against DUMMY_HASH (timing-safe)."""

    async def fake_get_user_by_username(_username):
        return None

    called = {"args": None}

    def fake_verify_password(plain_password, hashed_password_value):
        called["args"] = (plain_password, hashed_password_value)
        return False

    monkeypatch.setattr(authServices, "get_user_by_username", fake_get_user_by_username)
    monkeypatch.setattr(authServices, "verify_password", fake_verify_password)

    result = asyncio.run(authServices.authenticate_user("missing_user", "SomePass1!"))

    assert result is None
    assert called["args"] == ("SomePass1!", authServices.DUMMY_HASH)


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
@pytest.mark.xfail(reason="yet to confirm if we can create user with optional email/full_name fields")
def test_register_required_fields_only_success():
    """Test registration succeeds when only username and password are provided."""
    with TestClient(app) as client:
        username = f"user_{random_string()}"
        password = "MyPassword1!"

        response = client.post("/auth/register", json={
            "username": username,
            "password": password,
        })

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == username
        assert data.get("email") is None
        assert data.get("full_name") is None
        assert data["disabled"] is False


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
        # Use helper to register and login
        username, access_token, refresh_token = register_and_login(client)
        
        # Verify tokens are present and correct
        assert access_token is not None
        assert refresh_token is not None
        assert len(access_token) > 0
        assert len(refresh_token) > 0


def test_login_invalid_credentials():
    """Test that wrong password returns 401."""
    with TestClient(app) as client:
        # Register a user via helper (implicitly successful)
        username, _, _ = register_and_login(client)

        # Login with wrong password
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
        # Use helper to register and login
        username, access_token, _ = register_and_login(client)

        # Access /auth/me with the token
        response = client.get("/auth/me", headers={
            "Authorization": f"Bearer {access_token}"
        })

        assert response.status_code == 200
        assert response.json()["username"] == username


def test_me_with_refresh_token_returns_401():
    """/auth/me should reject refresh tokens (wrong token type)."""
    with TestClient(app) as client:
        _, _, refresh_token = register_and_login(client)

        response = client.get("/auth/me", headers={
            "Authorization": f"Bearer {refresh_token}"
        })

        assert response.status_code == 401


def test_me_with_malformed_token_returns_401():
    """/auth/me should reject malformed bearer tokens."""
    with TestClient(app) as client:
        response = client.get("/auth/me", headers={
            "Authorization": "Bearer definitely-not-a-jwt"
        })

        assert response.status_code == 401


def test_me_with_expired_access_token_returns_401():
    """/auth/me should reject expired access tokens."""
    with TestClient(app) as client:
        username = f"user_{random_string()}"
        password = "MyPassword1!"
        client.post("/auth/register", json={
            "username": username,
            "password": password,
            "email": f"{username}@example.com"
        })

        expired_access_token = create_access_token(
            data={"sub": username},
            expires_delta=timedelta(minutes=-1),
        )

        response = client.get("/auth/me", headers={
            "Authorization": f"Bearer {expired_access_token}"
        })

        assert response.status_code == 401


def test_me_with_disabled_user_returns_400(monkeypatch):
    """/auth/me should return inactive-user error for disabled accounts."""
    username = f"user_{random_string()}"

    async def fake_get_user_by_username(requested_username: str):
        if requested_username != username:
            return None
        return UserInDB(
            username=username,
            email=f"{username}@example.com",
            full_name="Disabled User",
            disabled=True,
            hashed_password="unused",
            created_at=datetime.now(timezone.utc),
        )

    monkeypatch.setattr(
        "src.app.services.authServices.get_user_by_username",
        fake_get_user_by_username,
    )

    with TestClient(app) as client:
        access_token = create_access_token(data={"sub": username})

        response = client.get("/auth/me", headers={
            "Authorization": f"Bearer {access_token}"
        })

        assert response.status_code == 400
        assert response.json()["detail"] == "Inactive user"


def test_me_with_deleted_user_returns_401(monkeypatch):
    """/auth/me should return 401 if token subject no longer exists."""
    username = f"user_{random_string()}"

    async def fake_get_user_by_username(_: str):
        return None

    monkeypatch.setattr(
        "src.app.services.authServices.get_user_by_username",
        fake_get_user_by_username,
    )

    with TestClient(app) as client:
        access_token = create_access_token(data={"sub": username})

        response = client.get("/auth/me", headers={
            "Authorization": f"Bearer {access_token}"
        })

        assert response.status_code == 401

def test_rate_limit():
    """Test that rate limiting works on the login endpoint."""
    with TestClient(app) as client:
        # Register the user via helper
        username, _, _ = register_and_login(client)
        
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


def test_refresh_with_access_token():
    """Test that using an access token for refresh returns 401."""
    with TestClient(app) as client:
        _, access_token, _ = register_and_login(client)

        # Try to refresh with access token instead of refresh token
        response = client.post("/auth/refresh", json={"refresh_token": access_token})
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid or expired refresh token"


def test_refresh_with_malformed_token():
    """Test that a malformed token string returns 401."""
    with TestClient(app) as client:
        response = client.post("/auth/refresh", json={"refresh_token": "not.a.valid.jwt"})
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid or expired refresh token"


def test_refresh_with_garbage_token():
    """Test that a garbage token string returns 401."""
    with TestClient(app) as client:
        response = client.post("/auth/refresh", json={"refresh_token": "garbage_string_no_dots"})
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid or expired refresh token"


def test_refresh_missing_refresh_token_field():
    """Test that missing refresh_token in body returns 422."""
    with TestClient(app) as client:
        response = client.post("/auth/refresh", json={})
        assert response.status_code == 422


def test_refresh_success_returns_new_tokens():
    """Test that a successful refresh returns new access and refresh tokens."""
    with TestClient(app) as client:
        _, _, refresh_token = register_and_login(client)

        response = client.post("/auth/refresh", json={"refresh_token": refresh_token})

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        # New tokens should be different from old ones
        assert data["refresh_token"] != refresh_token


def test_refresh_new_access_is_valid():
    """Test that the new access token from refresh can be used immediately."""
    with TestClient(app) as client:
        username, _, refresh_token = register_and_login(client)

        # Refresh to get new access token
        refresh_res = client.post("/auth/refresh", json={"refresh_token": refresh_token})
        new_access_token = refresh_res.json()["access_token"]

        # Use new access token on /auth/me
        me_res = client.get("/auth/me", headers={
            "Authorization": f"Bearer {new_access_token}"
        })

        assert me_res.status_code == 200
        assert me_res.json()["username"] == username


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


def test_logout_without_access_token():
    """Test that logout without Authorization header returns 401."""
    with TestClient(app) as client:
        _, _, refresh_token = register_and_login(client)

        response = client.post("/auth/logout",
            json={"refresh_token": refresh_token},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"


def test_logout_missing_refresh_token_body():
    """Test that logout with missing refresh_token in body returns 422."""
    with TestClient(app) as client:
        _, access_token, _ = register_and_login(client)

        response = client.post("/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"},
            json={},
        )
        assert response.status_code == 422


def test_logout_with_malformed_refresh_token():
    """Test that logout with malformed refresh token still succeeds (token is ignored gracefully)."""
    with TestClient(app) as client:
        _, access_token, _ = register_and_login(client)

        response = client.post("/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"refresh_token": "garbage_no_dots_token"},
        )
        # Revoke handles invalid tokens gracefully, so logout succeeds
        assert response.status_code == 204


def test_logout_invalidates_refresh_token():
    """Test that after logout, the refresh token cannot be used."""
    with TestClient(app) as client:
        _, access_token, refresh_token = register_and_login(client)

        # Logout revokes both tokens
        client.post("/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"refresh_token": refresh_token},
        )

        # Try to use the old refresh token to get new tokens
        response = client.post("/auth/refresh", json={"refresh_token": refresh_token})
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid or expired refresh token"


def test_logout_with_wrong_token_type():
    """Test that logout with a refresh token used as access token returns 401."""
    with TestClient(app) as client:
        _, _, refresh_token = register_and_login(client)

        # Try to use refresh token as access (Authorization header)
        response = client.post("/auth/logout",
            headers={"Authorization": f"Bearer {refresh_token}"},
            json={"refresh_token": refresh_token},
        )
        assert response.status_code == 401


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
