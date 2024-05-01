import uuid
from sqlalchemy import Boolean, Column, String, UUID, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    created_ad = Column(DateTime(False))
    login = Column(String(255), unique=True)
    password = Column(String(128))
    project_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    env = Column(String(255))
    domain = Column(String(255))
    locktime = Column(Boolean,default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)