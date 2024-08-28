from db.db_build import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, validates


class Event(Base):
    __tablename__ = "event_list"

    id_event = Column(
        Integer, nullable=False, primary_key=True, autoincrement=True
    )
    date = Column(DateTime, nullable=False)
    eventname = Column(String(15), nullable=False)
    comment = Column(String, nullable=False, required=False)
    user_id = mapped_column(ForeignKey("user_list.id"))

