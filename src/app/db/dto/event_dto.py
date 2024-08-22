from pydantic import BaseModel, EmailStr, Field


class BaseEventDto(BaseModel):
    login: str
    username: str
    eventname: str = Field(..., max_length=15)
    comment : str
    date: str

class CreateEventDto(BaseEventDto):
    pass


class EventDto(BaseEventDto):
    id: int

