from pydantic import BaseModel, EmailStr, Field


class CreateEventPayload(BaseModel):
    login: str
    email: EmailStr
    password: str
    date: str
    name: str = Field(..., max_length=15)
    commment: str


class EventPayload(BaseModel):
    login: str
    id: int
    date: str
    name: str = Field(..., max_length=15)
    commment: str


class EventResponse(BaseModel):
    user: str
    login: str
    date: str
    name: str = Field(..., max_length=15)
    commment: str
    id: int
