from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.schemas.base_entity import BaseEntity


class Company(BaseEntity, Base):
    __tablename__ = "company"

    name = Column(String(255), nullable=False)
    description = Column(String(255))

    users = relationship("User", back_populates="company")
