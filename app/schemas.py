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
    id : UUID
    locktime : bool
    

    class Config:
        orm_model = True
        
        

