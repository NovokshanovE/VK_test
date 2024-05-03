import datetime
import uuid
from sqlalchemy import Column, String, UUID, DateTime, TIMESTAMP
from .database import Base
import bcrypt


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_ad = Column(DateTime(False), default=datetime.datetime.now())
    login = Column(String(255), unique=True)
    password = Column(String(255))
    project_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    env = Column(String(255))
    domain = Column(String(255))
    locktime = Column(DateTime(False), default=None)

    def set_password(password):

        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return password

    def check_password(self, password):
        valid = bcrypt.checkpw(password.encode(), self.password)
        return valid
