from typing import List, Optional
from pydantic import BaseModel


class DataBase(BaseModel):
    ox: int  
    bpm: int

class DataCreate(DataBase):
    pass

class Data(DataBase):
    id: int
    class Config:
        orm_mode = True



class UserBase(BaseModel):
    name: str
    cpf: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True
