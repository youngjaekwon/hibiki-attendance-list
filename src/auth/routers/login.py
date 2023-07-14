from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.auth.exceptions import CredentialsException, InactiveUserException
from src.auth.schemas.token import RefreshToken, Token
from src.auth.services.login_serviece import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)
from src.auth.services.user_service import get_user_by_email
from src.database import get_db

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise CredentialsException
    elif not user.is_active:
        raise InactiveUserException
    access_token = create_access_token(jsonable_encoder(user))
    refresh_token = create_refresh_token(jsonable_encoder(user))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=Token)
async def token_refresh(
    body: Annotated[RefreshToken, Body(...)],
    db: Session = Depends(get_db),
):
    result = verify_refresh_token(body.refresh_token)
    if not result:
        raise CredentialsException
    user = get_user_by_email(db, body.email)
    if not user:
        raise CredentialsException
    elif not user.is_active:
        raise InactiveUserException
    access_token = create_access_token(jsonable_encoder(user))
    return {
        "access_token": access_token,
        "refresh_token": body.refresh_token,
        "token_type": "bearer",
    }


"""
TODO
- [ ] Recover password
- [ ] Reset Password
- [ ] Logout
"""
