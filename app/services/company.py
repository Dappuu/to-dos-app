from uuid import UUID
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exception import ResourceNotFoundError
from app.schemas.company import Company
from app.models.company import (
    CreateCompanyRequest,
    SearchCompanyModel,
    UpdateCompanyRequest,
)

logger = logging.getLogger(__name__)


async def get_Companies(
    db: AsyncSession, conditions: SearchCompanyModel
) -> list[Company]:
    query = select(Company)

    if conditions.company_id is not None:
        query = query.filter(Company.id == conditions.company_id)

    if conditions.company_name is not None:
        query = query.filter(Company.name.ilike(f"%{conditions.company_name}%"))

    query = query.offset((conditions.page - 1) * conditions.size).limit(conditions.size)

    compiled_query = query.compile()
    logger.debug(msg=str(compiled_query))

    result = await db.execute(query)
    companies = result.scalars().all()

    return companies


async def get_Company_By_Id(db: AsyncSession, company_id: UUID) -> Company:
    query = select(Company).where(Company.id == company_id)
    result = await db.execute(query)
    company = result.scalar_one_or_none()

    if company is None:
        raise ResourceNotFoundError()

    return company


async def create_Company(
    db: AsyncSession, createRequest: CreateCompanyRequest
) -> Company:
    company = Company(**createRequest.model_dump())

    db.add(company)
    await db.commit()
    await db.refresh(company)

    return company


async def update_Company(
    db: AsyncSession, company_id: UUID, updateRequest: UpdateCompanyRequest
) -> Company:
    company = await get_Company_By_Id(db, company_id)

    company.name = updateRequest.name
    company.description = updateRequest.description

    await db.commit()
    await db.refresh(company)
    return company


async def delete_Company(db: AsyncSession, company_id: UUID):
    company = await get_Company_By_Id(db, company_id)

    if company is None:
        raise ResourceNotFoundError()

    await db.delete(company)
    await db.commit()
    return
