from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.spec import Specifications
from app.schemas.task import STATUS, Task


class TaskViewModel(BaseModel):
    id: UUID
    summary: str
    description: str
    status: STATUS
    priority: int
    doer_id: UUID
    assigner_id: UUID
    
