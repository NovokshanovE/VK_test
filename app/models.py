import uuid
from sqlalchemy import Boolean, Column, String, UUID

from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4, index=True)
    login = Column(String(255),index=True)
    name = Column(String(255),index=True)
    email = Column(String(255), unique=True, index=True)
    is_active = Column(Boolean,default=False)