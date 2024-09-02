from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exception import ResourceNotFoundError
from app.schemas.company import Company
from app.models.company import CompanyViewModel, CreateCompanyRequest, SearchCompanyModel, UpdateCompanyRequest

async def get_Companies(db: AsyncSession, conditions: SearchCompanyModel) -> list[Company]:
    query = select(Company)
    
    if not conditions.company_id:
        query.filter(Company.id == conditions.company_id)
        
    if not conditions.company_name:
        query.filter(Company.name.like(f"{conditions.company_name}"))
        
    query.offset((conditions.page - 1) * conditions.size ).limit(conditions.size)
        
    result = await db.execute(query)
    companies = result.scalars().all()
    
    return companies

async def get_Company_By_Id(db: AsyncSession, company_id: UUID) -> list[Company]:
    query = select(Company).where(Company.id == company_id)
    result = await db.execute(query)
    company = result.scalar_one_or_none()
    
    if not company:
        raise ResourceNotFoundError()
    
    return company

async def create_Company(db: AsyncSession, createRequest: CreateCompanyRequest) -> Company:
    company = Company(**createRequest.model_dump())
    
    db.add(company)
    await db.commit()
    await db.refresh(company)
    
    return company

async def update_Company(db: AsyncSession, company_id: UUID, updateRequest: UpdateCompanyRequest) -> Company:
    company = await get_Company_By_Id(db, company_id)
    
    if not company:
        raise ResourceNotFoundError()
    
    company.name = updateRequest.name
    company.description = updateRequest.description
    
    await db.commit()
    await db.refresh(company)
    return company

async def delete_Company(db: AsyncSession, company_id: UUID):
    company = await get_Company_By_Id(db, company_id)
    
    if not company:
        raise ResourceNotFoundError()
    
    await db.delete(company)
    await db.commit()
    return