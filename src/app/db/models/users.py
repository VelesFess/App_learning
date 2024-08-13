# Импорты всегда только абсолютные!!!
# # from ..db import Base
from sqlalchemy import  Column, Integer, String

from db.db import Base


#  id  |      email      | pass  |      name      |  login  
# -----+-----------------+-------+----------------+---------
#  201 | sarah@mail.com  | 12345 | Sarah Martinez | SarahM
#  202 | daniel@mail.com | 54321 | Daniel Lewis   | DanielL

# Обрати внимание: имплементирован Alembic (src/app/db/migrations)
class User(Base):
    __tablename__ = "user_list"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password  = Column(String, nullable=False)
    name = Column(String, nullable=False)
    login = Column(String, nullable=False)


# Это все должно быть в DTO
# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     login: str
#     password: str


# class User(UserBase):
#     id: int
#     email: str
#     name: str 
    

#     class Config:
#         orm_mode = True