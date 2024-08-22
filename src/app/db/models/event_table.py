from datetime import date

from db.db_build import Base
from sqlalchemy import Column, Integer, String


class Event(Base):
    __tablename__ = "event_list"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    login = Column(String, nullable=False, unique=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    date = Column(date.strftime("%Y-%m-%d"), nullable=False)
    eventname = Column(String(15), nullable=False)
    comment = Column(String, nullable=False)
