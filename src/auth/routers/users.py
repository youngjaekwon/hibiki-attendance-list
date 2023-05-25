from typing import Any

from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.auth import models
from src.auth.schemas.user import User as UserSchema, UserCreate, UserUpdate
from src.auth.dependencies import get_current_user
from src.auth.services import user_service
from src.auth.services.user_service import (
    get_users_multi,
    get_user_by_email,
    get_user_by_id,
)
from src.auth.exceptions import (
    UserAlreadyExistsException,
    UserNoPrivilegesException,
    UserDoesNotExistException,
)
from src.database import get_db

router = APIRouter()


@router.get("/", response_model=list[UserSchema])
async def retrieve_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> list[UserSchema]:
    """
    Retrieve users.
    """
    users = get_users_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserSchema)
async def create_user(
    db: Session = Depends(get_db),
    body: UserCreate = Body(...),
) -> UserSchema:
    """
    Create a new user.
    """
    user = get_user_by_email(db, email=body.email)
    if user:
        raise UserAlreadyExistsException
    user = user_service.create(db, body)
    user = UserSchema.from_orm(user)
    """
    TODO: Send email to user with activation link
    """
    return user


@router.get("/me", response_model=UserSchema)
async def retrieve_user_me(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> UserSchema:
    """
    Retrieve the current user.
    """
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_user_me(
    db: Session = Depends(get_db),
    body: UserUpdate = Body(...),
    current_user: models.User = Depends(get_current_user),
) -> UserSchema:
    """
    Update the current user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdate(**current_user_data)
    if body.password is not None:
        user_in.password = body.password
    user = update_user(db, current_user, user_in)
    return user


@router.get("/{user_id}", response_model=UserSchema)
async def retrieve_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Retrieve a user.
    """
    user = get_user_by_id(db, id=user_id)
    if user == current_user:
        pass
    elif not current_user.is_superuser:
        raise UserNoPrivilegesException
    return user


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: str,
    db: Session = Depends(get_db),
    body: UserUpdate = Body(...),
    current_user: models.User = Depends(get_current_user),
) -> UserSchema:
    """
    Update a user.
    """
    user = get_user_by_id(db, id=user_id)
    if not user:
        raise UserDoesNotExistException
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise UserNoPrivilegesException
    user_in = UserUpdate(**user.dict())
    if body.password is not None:
        user_in.password = body.password
    user = user_service.update(db, user, user_in)
    user = UserSchema.from_orm(user)
    return user
