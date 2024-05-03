from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class UserBase(BaseModel):
    login: str
    project_id: UUID
    env: str
    domain: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID
    # locktime : datetime
    created_ad: datetime

    class Config:
        orm_model = True


class UserLock(BaseModel):
    locktime: datetime
