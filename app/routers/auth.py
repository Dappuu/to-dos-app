from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_async_db_context
from app.exceptions import UnAuthorizedError
from app.services import auth as AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token")
async def login_for_access_token(
    data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db_context),
):
    user = await AuthService.authenticate_user(data.username, data.password, db)

    return {
        "access_token": AuthService.create_access_token(user, timedelta(minutes=30)),
        "token_type": "bearer",
    }
