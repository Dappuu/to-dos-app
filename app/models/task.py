from typing import Optional
from uuid import UUID
import uuid

from pydantic import BaseModel, ConfigDict

from app.schemas.task import STATUS


class TaskViewModel(BaseModel):
    id: UUID
    summary: str
    description: str
    status: STATUS
    priority: int
    assigner_id: UUID
    doer_id: UUID

    model_config = ConfigDict(from_attributes=True)


class CreateTaskRequest(BaseModel):
    summary: str
    description: Optional[str]
    priority: int
    doer_id: UUID

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "summary": "Sumary Task",
                "description": "This is description",
                "priority": 1,
                "doer_id": uuid.uuid4(),
            }
        },
    )


class UpdateTaskRequest(BaseModel):
    summary: str
    description: str
    status: STATUS
    priority: int
    doer_id: UUID

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "summary": "New Task",
                "description": "This is description",
                "priority": 2,
                "status": STATUS.IN_PROGRESS,
                "doer_id": uuid.uuid4(),
            }
        },
    )
