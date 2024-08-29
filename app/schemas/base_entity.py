from sqlalchemy import Column, UUID
import uuid

class BaseEntity:
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
