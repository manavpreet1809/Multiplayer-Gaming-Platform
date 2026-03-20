from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from src.app.schemas.auth import Token, UserCreate, UserPublic
from src.app.services.authServices import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    create_user,
    get_current_user,
    get_user_by_username,
    limiter,
    oauth2_scheme,
    revoke_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def register(user: UserCreate):
    try:
        return await create_user(user)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/login", response_model=TokenPair)
@limiter.limit("10/minute")
async def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(data={"sub": user.username})

    return TokenPair(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenPair)
@limiter.limit("20/minute")
async def refresh(request: Request, body: RefreshRequest):
    """Exchange a valid refresh token for a new access + refresh token pair."""
    username = await decode_refresh_token(body.refresh_token)
    user = await get_user_by_username(username)

    if user is None or user.disabled:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    # Revoke the consumed refresh token so it cannot be replayed
    await revoke_token(body.refresh_token)

    access_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    new_refresh_token = create_refresh_token(data={"sub": username})

    return TokenPair(access_token=access_token, refresh_token=new_refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    body: LogoutRequest,
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    access_token: Annotated[str, Depends(oauth2_scheme)],
):
    """
    Revoke both the current access token and the provided refresh token.
    Client must send:
      Authorization: Bearer <access_token>         (header)
      { "refresh_token": "<refresh_token>" }       (body)
    """
    await revoke_token(access_token)
    await revoke_token(body.refresh_token)


@router.get("/me", response_model=UserPublic)
async def read_me(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
):
    return current_user