from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    is_active: bool | None = True
    is_superuser: bool = False


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: str | None = None


class UserInDBBase(UserBase):
    id: UUID | None = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    ...


class UserInDB(UserInDBBase):
    hashed_password: str
