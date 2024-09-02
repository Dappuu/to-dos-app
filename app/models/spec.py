from pydantic import BaseModel, Field

class Specifications(BaseModel):
    page: int = Field(ge=1, default=1)
    size: int = Field(ge=1, le=50, default=12)