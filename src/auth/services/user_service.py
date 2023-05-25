from uuid import UUID

from sqlalchemy.orm import Session

from src.auth.models import User
from src.auth.schemas.user import UserCreate, UserUpdate
from src.auth.utils.security import get_password_hash


def get_user_by_id(db: Session, id: UUID) -> User:
    return db.query(User).filter(User.id == id).first()


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def get_users_multi(db: Session, *, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create(
    db: Session,
    user_in: UserCreate,
) -> User:
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(
    db: Session,
    user: User,
    user_in: UserUpdate | dict[str, any],
) -> User:
    if isinstance(user_in, dict):
        update_data = user_in
    else:
        update_data = user_in.dict(exclude_unset=True)
    if update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
    for field in update_data:
        setattr(user, field, update_data[field])
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
