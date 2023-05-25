from fastapi import APIRouter

from .routers import login, users

auth_router = APIRouter()
auth_router.include_router(login.router, tags=["login"])
auth_router.include_router(users.router, prefix="/users", tags=["users"])
