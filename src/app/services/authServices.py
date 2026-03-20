import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.app.db.validUser_mongo import users_collection
from src.app.schemas.auth import TokenData, UserCreate, UserInDB, UserPublic

# Fix: enforce SECRET_KEY — refuse to start with the insecure default
SECRET_KEY = os.getenv("SECRET_KEY", "")
if not SECRET_KEY or SECRET_KEY == "CHANGE_ME_TO_A_LONG_RANDOM_SECRET":
    raise RuntimeError(
        "SECRET_KEY environment variable is not set or is still the default. "
        "Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("not-the-real-password")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Rate limiter (attach to FastAPI app with app.state.limiter = limiter)
limiter = Limiter(key_func=get_remote_address)


def verify_password(plain_password: str, hashed_password_value: str) -> bool:
    return password_hash.verify(plain_password, hashed_password_value)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """Long-lived refresh token so users aren't hard-logged-out every 30 minutes."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_refresh_token(token: str) -> str:
    """Validate a refresh token and return the username it encodes."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise credentials_exception
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except InvalidTokenError:
        raise credentials_exception


async def get_user_by_username(username: str) -> UserInDB | None:
    doc = await users_collection.find_one({"username": username})
    if not doc:
        return None
    return UserInDB(
        username=doc["username"],
        email=doc.get("email"),
        full_name=doc.get("full_name"),
        disabled=doc.get("disabled", False),
        hashed_password=doc["hashed_password"],
        created_at=doc["created_at"],
    )


async def create_user(user: UserCreate) -> UserPublic:
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise ValueError("Username already exists")

    user_doc = {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": get_password_hash(user.password),
        "disabled": False,
        "created_at": datetime.now(timezone.utc),
    }
    await users_collection.insert_one(user_doc)

    return UserPublic(
        username=user_doc["username"],
        email=user_doc["email"],
        full_name=user_doc["full_name"],
        disabled=user_doc["disabled"],
    )


async def authenticate_user(username: str, password: str) -> UserInDB | None:
    user = await get_user_by_username(username)

    if not user:
        # Timing-safe: always run a hash verify to prevent username enumeration
        verify_password(password, DUMMY_HASH)
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserPublic:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise credentials_exception
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = await get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception

    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return UserPublic(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        disabled=user.disabled,
    )