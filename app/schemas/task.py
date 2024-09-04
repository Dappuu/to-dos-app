import enum
from sqlalchemy import Column, String, Enum, Integer, Uuid, ForeignKey
from sqlalchemy.orm import relationship

from app.schemas.base_entity import BaseEntity
from app.database import Base


class STATUS(enum.Enum):
    NEW = "N"
    IN_PROGRESS = "IP"
    PENDING = "P"
    ABANDONED = "A"
    DONE = "D"


class Task(Base, BaseEntity):
    __tablename__ = "task"

    summary = Column(String(255))
    description = Column(String(255))
    status = Column(Enum(STATUS), nullable=False, default=STATUS.NEW)
    priority = Column(Integer, nullable=False)

    assigner_id = Column(Uuid(as_uuid=True), ForeignKey("user.id"), nullable=False)
    assigner = relationship(
        "User", foreign_keys=[assigner_id], back_populates="assigned_tasks"
    )

    doer_id = Column(Uuid(as_uuid=True), ForeignKey("user.id"), nullable=False)
    doer = relationship("User", foreign_keys=[doer_id], back_populates="tasks_to_do")
