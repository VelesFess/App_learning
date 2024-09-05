from datetime import datetime

from pydantic import BaseModel, Field


class BaseEventDto(BaseModel):
    user_id: int
    eventname: str = Field(..., max_length=15)
    comment: str
    date: datetime


class CreateEventDto(BaseEventDto):
    pass


class EventDto(BaseEventDto):
    id_event: int
