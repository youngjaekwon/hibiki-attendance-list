from sqlalchemy import Boolean, Column, String, UUID

from src.database import Base


class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    username = Column(String, index=True)
