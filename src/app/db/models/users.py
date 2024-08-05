from ..db import Base
from pydantic import BaseModel
from sqlalchemy import  Column, Integer, String


#  id  |      email      | pass  |      name      |  login  
# -----+-----------------+-------+----------------+---------
#  201 | sarah@mail.com  | 12345 | Sarah Martinez | SarahM
#  202 | daniel@mail.com | 54321 | Daniel Lewis   | DanielL

class User(Base):
    __tablename__ = "user_list"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password  = Column(String)
    name = Column(String)
    login = Column(String)


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    login: str
    password: str


class User(UserBase):
    id: int
    email: str
    name: str 
    

    class Config:
        orm_mode = True