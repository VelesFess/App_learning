from datetime import date

from db.db_build import Base
from sqlalchemy import Column, Integer, String


class Event(Base):
    __tablename__ = "user_list"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user = Column(String, nullable=False, unique=True, index=True)
    date = Column(date, nullable=False)
    name = Column(String(15), nullable=False)
    comment = Column(String, nullable=False)
