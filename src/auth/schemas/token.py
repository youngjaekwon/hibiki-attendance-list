from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    sub: UUID | None = None


class RefreshToken(BaseModel):
    email: str
    refresh_token: str
