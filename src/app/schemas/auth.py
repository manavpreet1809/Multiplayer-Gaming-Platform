from datetime import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    email: str | None = None
    full_name: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None

class UserPublic(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool = False

class UserInDB(UserPublic):
    hashed_password: str
    created_at: datetime



