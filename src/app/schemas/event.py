from pydantic import BaseModel, EmailStr, Field


class CreateEventPayload(BaseModel):
    username: str
    login: str
    email: EmailStr
    password: str
    date: str
    eventname: str = Field(..., max_length=15)
    comment: str


class EventPayload(BaseModel):
    login: str
    id: int
    date: str
    eventname: str = Field(..., max_length=15)
    commment: str


class EventResponse(BaseModel):
    username: str
    login: str
    date: str
    eventname: str = Field(..., max_length=15)
    commment: str
    id: int
