from datetime import timedelta
from typing import Optional
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError

from app.utils import *
from app.settings import JWT_SECRET, JWT_ALGORITHM
from app.schemas import User
from app.exceptions import TokenError, InactiveError, UnAuthorizedError


async def authenticate_user(username: str, password: str, db: AsyncSession) -> User:
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    user = result.scalar()

    if not (user and verify_password(password, user.hashed_password)):
        raise UnAuthorizedError()
    return user


def create_access_token(user: User, expires: Optional[timedelta] = None):
    claims = {
        "sub": user.username,
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_admin": user.is_admin,
        "is_active": user.is_active,
    }
    expire = (
        get_current_utc_time() + expires
        if expires
        else get_current_utc_time() + timedelta(minutes=10)
    )
    claims.update({"exp": expire})
    return jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)


oa2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


def token_interceptor(token: str = Depends(oa2_bearer)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user = User()
        user.username = payload.get("sub")
        user.id = UUID(payload.get("id"))
        user.first_name = payload.get("first_name")
        user.last_name = payload.get("last_name")
        user.is_admin = payload.get("is_admin")
        user.is_active = payload.get("is_active")

        if user.username is None or user.id is None:
            raise TokenError()
        if user.is_active is None:
            raise InactiveError()
        return user
    except JWTError:
        raise TokenError()
