from db.db_build import Base
from sqlalchemy import Column, Integer, String

#  id  |      email      | pass  |      name      |  login
# -----+-----------------+-------+----------------+---------
#  201 | sarah@mail.com  | 12345 | Sarah Martinez | SarahM
#  202 | daniel@mail.com | 54321 | Daniel Lewis   | DanielL


class User(Base):
    __tablename__ = "user_list"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    login = Column(String, nullable=False)
