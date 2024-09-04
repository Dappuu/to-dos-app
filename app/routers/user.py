from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db_context
from app.exceptions.exception import AccessDeniedError
from app.models.user import (
    CreateUserRequest,
    SearchUserModel,
    UpdateUserRequest,
    UserViewModel,
)
from app.schemas.user import User
from app.services import user as UserService
from app.services import auth as AuthService
from app.utils.password import generate_password


router = APIRouter(prefix="/user", tags=["User"])


@router.get("", response_model=list[UserViewModel])
async def get_All_Users(
    user_id: UUID = Query(default=None),
    username: str = Query(default=None),
    email: str = Query(default=None),
    is_active: bool = Query(default=None),
    is_admin: bool = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    db: AsyncSession = Depends(get_async_db_context),
):
    conditions = SearchUserModel(
        user_id=user_id,
        username=username,
        email=email,
        is_active=is_active,
        is_admin=is_admin,
        page=page,
        size=size,
    )

    users = await UserService.get_Users(db, conditions)
    return [UserViewModel.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserViewModel)
async def get_User_By_Id(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db_context),
):
    company = await UserService.get_User_By_Id(db, user_id)

    return UserViewModel.model_validate(company)


@router.post("", status_code=status.HTTP_200_OK, response_model=UserViewModel)
async def create_User(
    createRequest: CreateUserRequest,
    db: AsyncSession = Depends(get_async_db_context),
    loggin_user: User = Depends(AuthService.token_interceptor),
):
    if not loggin_user.is_admin:
        raise AccessDeniedError()

    password = generate_password()
    user = await UserService.create_User(db, createRequest, password)
    return UserViewModel.model_validate(user)


@router.put(
    "/{user_id}", status_code=status.HTTP_201_CREATED, response_model=UserViewModel
)
async def update_User(
    user_id: UUID,
    updateRequest: UpdateUserRequest,
    db: AsyncSession = Depends(get_async_db_context),
    loggin_user: User = Depends(AuthService.token_interceptor),
):
    if not loggin_user.is_admin:
        raise AccessDeniedError()

    user = await UserService.update_User(db, user_id, updateRequest)
    return UserViewModel.model_validate(user)


@router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_User(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db_context),
    loggin_user: User = Depends(AuthService.token_interceptor),
):
    if not loggin_user.is_admin:
        raise AccessDeniedError()

    await UserService.delete_User(db, user_id)
    return
