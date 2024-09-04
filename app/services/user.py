from uuid import UUID
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exception import ResourceNotFoundError
from app.models.user import CreateUserRequest, SearchUserModel, UpdateUserRequest
from app.schemas.user import User
from app.utils.password import get_password_hash

logger = logging.getLogger(__name__)


async def get_Users(db: AsyncSession, conditions: SearchUserModel) -> list[User]:
    query = select(User)

    if conditions.user_id is not None:
        query = query.filter(User.id == conditions.user_id)

    if conditions.username is not None:
        query = query.filter(User.username.ilike(f"%{conditions.username}%"))

    if conditions.email is not None:
        query = query.filter(User.email.ilike(f"%{conditions.email}%"))

    if conditions.is_active is not None:
        query = query.filter(User.is_active == conditions.is_active)

    if conditions.is_admin is not None:
        query = query.filter(User.is_admin == conditions.is_admin)

    query = query.offset((conditions.page - 1) * conditions.size).limit(conditions.size)

    compiled_query = query.compile()
    logger.debug(msg=str(compiled_query))

    result = await db.execute(query)
    users = result.scalars().all()

    return users


async def get_User_By_Id(db: AsyncSession, user_id: UUID) -> User:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise ResourceNotFoundError()

    return user


async def create_User(db: AsyncSession, createRequest: CreateUserRequest) -> User:
    user_data = createRequest.model_dump()
    user_data["hashed_password"] = get_password_hash(user_data["password"])
    user_data.pop("password")
    user = User(**user_data)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def update_User(
    db: AsyncSession, user_id: UUID, updateRequest: UpdateUserRequest
) -> User:
    user = await get_User_By_Id(db, user_id)

    user.first_name = updateRequest.first_name
    user.last_name = updateRequest.last_name
    user.is_admin = updateRequest.is_admin
    user.is_active = updateRequest.is_active

    await db.commit()
    await db.refresh(user)
    return user


async def delete_User(db: AsyncSession, user_id: UUID):
    user = await get_User_By_Id(db, user_id)

    if not user:
        raise ResourceNotFoundError()

    await db.delete(user)
    await db.commit()
    return
