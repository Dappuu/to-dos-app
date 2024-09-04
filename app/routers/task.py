from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db_context
from app.exceptions.exception import AccessDeniedError
from app.models.task import CreateTaskRequest, TaskViewModel, UpdateTaskRequest

from app.schemas.user import User
from app.services import task as TaskService
from app.services import auth as AuthService


router = APIRouter(prefix="/task", tags=["Task"])


@router.get("/{user_id}", response_model=list[TaskViewModel])
async def get_Tasks_By_User_Id(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db_context),
    _: User = Depends(AuthService.token_interceptor),
):
    tasks = await TaskService.get_Tasks_By_User_Id(db, user_id)

    return [TaskViewModel.model_validate(task) for task in tasks]


@router.post("", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
async def create_Task(
    createRequest: CreateTaskRequest,
    db: AsyncSession = Depends(get_async_db_context),
    user: User = Depends(AuthService.token_interceptor),
):

    task = await TaskService.create_Task(db, createRequest, user.id)
    return TaskViewModel.model_validate(task)


@router.put(
    "/{task_id}", status_code=status.HTTP_201_CREATED, response_model=TaskViewModel
)
async def update_Task(
    task_id: UUID,
    updateRequest: UpdateTaskRequest,
    db: AsyncSession = Depends(get_async_db_context),
    _: User = Depends(AuthService.token_interceptor),
):

    task = await TaskService.update_Task(db, task_id, updateRequest)
    return TaskViewModel.model_validate(task)


@router.delete(
    "/{task_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_Task(
    task_id: UUID,
    db: AsyncSession = Depends(get_async_db_context),
    _: User = Depends(AuthService.token_interceptor),
):

    await TaskService.delete_Task(db, task_id)
    return
