from pydantic import BaseModel, EmailStr, Field


class BaseEventDto(BaseModel):
    user_id : int
    eventname: str = Field(..., max_length=15)
    comment: str
    date: str


class CreateEventDto(BaseEventDto):
    pass


class EventDto(BaseEventDto):
    id_event: int
