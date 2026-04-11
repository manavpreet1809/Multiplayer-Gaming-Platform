import re
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


PASSWORD_RULES = (
    (r".{8,}",          "at least 8 characters"),
    (r"[A-Z]",          "at least one uppercase letter"),
    (r"[a-z]",          "at least one lowercase letter"),
    (r"\d",             "at least one digit"),
    (r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]", "at least one special character"),
)


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr | None = None
    full_name: str | None = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        failures = [
            msg for pattern, msg in PASSWORD_RULES
            if not re.search(pattern, v)
        ]
        if failures:
            raise ValueError("Password must contain " + ", ".join(failures))
        return v





class PasswordResetRequest(BaseModel):
    identifier: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        failures = [
            msg for pattern, msg in PASSWORD_RULES
            if not re.search(pattern, v)
        ]
        if failures:
            raise ValueError("Password must contain " + ", ".join(failures))
        return v


class TokenData(BaseModel):
    username: str | None = None
    jti: str | None = None


class UserPublic(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool = False
    stats: dict = Field(default_factory=lambda: {
        "overall": {
            "games_played": 0,
            "wins": 0,
            "losses": 0,
            "ties": 0,
            "mmr": 1000,
            "rank": "Bronze",
        },
        "games": {
            "chess": {
                "games_played": 0,
                "wins": 0,
                "losses": 0,
                "ties": 0,
                "mmr": 1000,
                "rank": "Bronze",
            },
            "tictactoe": {
                "games_played": 0,
                "wins": 0,
                "losses": 0,
                "ties": 0,
                "mmr": 1000,
                "rank": "Bronze",
            },
        },
    })


class UserInDB(UserPublic):
    hashed_password: str
    created_at: datetime