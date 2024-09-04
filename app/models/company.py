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



class CreateCompanyRequest(BaseModel):
    name: str
    description: Optional[str]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"name": "NashTech", "description": "This is a great company!"}
        },
    )


class UpdateCompanyRequest(BaseModel):
    name: str
    description: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"name": "Example Corp", "description": "An example company"}
        },
    )
