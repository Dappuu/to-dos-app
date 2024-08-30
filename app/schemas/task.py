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

    user_id = Column(Uuid, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="tasks")
