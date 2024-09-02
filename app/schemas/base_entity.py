import uuid

from sqlalchemy import Column, Uuid

class BaseEntity:
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
