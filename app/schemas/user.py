from sqlalchemy import Boolean, Column, ForeignKey, String, UUID
from sqlalchemy.orm import relationship

from app.schemas.base_entity import BaseEntity
from app.database import Base


class User(BaseEntity, Base):
    __tablename__ = "user"

    email = Column(String(255))
    username = Column(String(255), unique=True, index=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    company_id = Column(UUID, ForeignKey("company.id"), nullable=False)
    company = relationship("Company", back_populates="users")

    tasks = relationship("Task", back_populates="user")
