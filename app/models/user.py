from typing import Optional
from uuid import UUID
import uuid

from pydantic import BaseModel, ConfigDict

from app.models.spec import Specifications


class UserViewModel(BaseModel):
    id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    company_id: UUID
    is_admin: bool
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class SearchUserModel(Specifications):
    user_id: Optional[str]
    username: Optional[str]
    email: Optional[str]
    is_active: Optional[bool]
    is_admin: Optional[bool]


class CreateUserRequest(BaseModel):
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    company_id: UUID
    is_admin: bool

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "user1",
                "password": "password@123",
                "email": "user1@gmail.com",
                "first_name": "Dat",
                "last_name": "Bui Viet",
                "is_admin": True,
                "company_id": uuid.uuid4(),
            }
        },
    )


class UpdateUserRequest(BaseModel):
    first_name: str
    last_name: str
    is_admin: bool
    is_active: bool

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "Dat",
                "last_name": "Bui Viet",
                "is_admin": True,
                "is_active": False,
            }
        },
    )
