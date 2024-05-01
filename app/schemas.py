from uuid import UUID
from pydantic import BaseModel, SecretStr

class UserBase(BaseModel):
    login: str
    project_id: UUID
    env: str
    domain: str

class UserCreate(UserBase):
    password: SecretStr

class User(UserBase):
    id : UUID
    locktime : bool
    

    class Config:
        orm_model = True
        
        

