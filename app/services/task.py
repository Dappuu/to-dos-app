from uuid import UUID
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exception import ResourceNotFoundError
from app.models.task import CreateTaskRequest, UpdateTaskRequest
from app.schemas.task import Task

logger = logging.getLogger(__name__)


async def get_Tasks_By_User_Id(db: AsyncSession, user_id: UUID) -> list[Task]:
    query = select(Task).where(Task.doer_id == user_id)
    result = await db.execute(query)
    tasks = result.scalars().all()

    return tasks


async def get_Task_By_Id(db: AsyncSession, task_id: UUID) -> Task:
    query = select(Task).where(Task.id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    if task is None:
        raise ResourceNotFoundError()

    return task


async def create_Task(
    db: AsyncSession, createRequest: CreateTaskRequest, user_Id: UUID
) -> Task:
    task = Task(**createRequest.model_dump())
    task.assigner_id = user_Id

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task


async def update_Task(
    db: AsyncSession, task_id: UUID, updateRequest: UpdateTaskRequest
) -> Task:
    task = await get_Task_By_Id(db, task_id)

    task.summary = updateRequest.summary
    task.description = updateRequest.description
    task.status = updateRequest.status
    task.priority = updateRequest.priority
    task.doer_id = updateRequest.doer_id

    await db.commit()
    await db.refresh(task)
    return task


async def delete_Task(db: AsyncSession, task_id: UUID):
    user = await get_Task_By_Id(db, task_id)

    if not user:
        raise ResourceNotFoundError()

    await db.delete(user)
    await db.commit()
    return
