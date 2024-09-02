from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.spec import Specifications


class CompanyViewModel(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class SearchCompanyModel(Specifications):
    company_id: Optional[str] = None
    company_name: Optional[str] = None

    def __init__(self, company_id=None, company_name=None, page=1, size=12):
        super().__init__(
            company_id=company_id,
            company_name=company_name,
            page=page,
            size=size,
        )


class CreateCompanyRequest(BaseModel):
    name: str
    description: Optional[str]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {"name": "NashTech", "description": "This is a great company!"}
        },
    )


class UpdateCompanyRequest(BaseModel):
    name: str
    description: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {"name": "Example Corp", "description": "An example company"}
        },
    )
