from sqlalchemy import Boolean, Column, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship

from app.schemas.base_entity import BaseEntity
from app.database import Base
from app.schemas.task import Task


class User(BaseEntity, Base):
    __tablename__ = "user"

    email = Column(String(255))
    username = Column(String(255), unique=True, index=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    company_id = Column(Uuid(as_uuid=True), ForeignKey("company.id"), nullable=False)
    company = relationship("Company", back_populates="users")

    # Tasks assigned by this user
    assigned_tasks = relationship("Task", foreign_keys=[Task.assigner_id], back_populates="assigner")

    # Tasks to be done by this user
    tasks_to_do = relationship("Task", foreign_keys=[Task.doer_id], back_populates="doer")
