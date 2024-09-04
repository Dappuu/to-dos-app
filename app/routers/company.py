from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db_context
from app.exceptions.exception import AccessDeniedError
from app.models.company import (
    CompanyViewModel,
    CreateCompanyRequest,
    SearchCompanyModel,
    UpdateCompanyRequest,
)
from app.schemas.user import User
from app.services import company as CompanyService
from app.services import auth as AuthService


router = APIRouter(prefix="/company", tags=["Company"])


@router.get("", response_model=list[CompanyViewModel])
async def get_All_Companies(
    company_id: UUID = Query(default=None),
    company_name: str = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    db: AsyncSession = Depends(get_async_db_context),
    user: User = Depends(AuthService.token_interceptor),
):

    if not user.is_admin:
        raise AccessDeniedError()

    conditions = SearchCompanyModel(
        company_id=company_id, company_name=company_name, page=page, size=size
    )

    companies = await CompanyService.get_Companies(db, conditions)
    return [CompanyViewModel.model_validate(company) for company in companies]


@router.get("/{company_id}", response_model=CompanyViewModel)
async def get_Company_By_Id(
    company_id: UUID,
    db: AsyncSession = Depends(get_async_db_context),
    user: User = Depends(AuthService.token_interceptor),
):
    if not user.is_admin:
        raise AccessDeniedError()

    company = await CompanyService.get_Company_By_Id(db, company_id)

    return CompanyViewModel.model_validate(company)


@router.post("", status_code=status.HTTP_200_OK, response_model=CompanyViewModel)
async def create_Company(
    createRequest: CreateCompanyRequest,
    db: AsyncSession = Depends(get_async_db_context),
    user: User = Depends(AuthService.token_interceptor),
):
    if not user.is_admin:
        raise AccessDeniedError()

    company = await CompanyService.create_Company(db, createRequest)
    return CompanyViewModel.model_validate(company)


@router.put(
    "/{company_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=CompanyViewModel,
)
async def update_Company(
    company_id: UUID,
    updateRequest: UpdateCompanyRequest,
    db: AsyncSession = Depends(get_async_db_context),
    user: User = Depends(AuthService.token_interceptor),
):
    if not user.is_admin:
        raise AccessDeniedError()

    company = await CompanyService.update_Company(db, company_id, updateRequest)
    return CompanyViewModel.model_validate(company)


@router.delete(
    "/{company_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_Company(
    company_id: UUID,
    db: AsyncSession = Depends(get_async_db_context),
    user: User = Depends(AuthService.token_interceptor),
):
    if not user.is_admin:
        raise AccessDeniedError()

    await CompanyService.delete_Company(db, company_id)
    return
