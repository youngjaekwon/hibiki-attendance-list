from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.auth.models import User
from src.auth.services.user_service import get_user_by_email
from src.auth.exceptions import CredentialsException, InactiveUserException
from src.auth.utils.security import SCRET_KEY, ALGORITHM
from src.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(token, SCRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise CredentialsException
    except JWTError:
        raise CredentialsException
    user = get_user_by_email(db, email=email)

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise InactiveUserException
    return current_user
