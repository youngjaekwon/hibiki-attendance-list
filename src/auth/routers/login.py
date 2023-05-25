from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database import get_db
from src.auth.exceptions import CredentialsException, InactiveUserException
from src.auth.schemas.token import Token
from src.auth.services.login_serviece import authenticate_user, create_access_token

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise CredentialsException
    elif not user.is_active:
        raise InactiveUserException
    access_tokne = create_access_token(data={"sub": user.email})
    return {"access_token": access_tokne, "token_type": "bearer"}


"""
TODO
- [ ] Recover password
- [ ] Refresh token
- [ ] Reset Password
- [ ] Logout
"""
