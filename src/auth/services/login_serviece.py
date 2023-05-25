from datetime import datetime, timedelta

from jose import jwt
from sqlalchemy.orm import Session


from src.auth.models import User
from src.auth.services.user_service import get_user_by_email
from src.auth.utils.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SCRET_KEY,
    ALGORITHM,
    verify_password,
)


def authenticate_user(db: Session, email, password: str) -> User | bool:
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SCRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
