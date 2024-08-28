from db.dto.event_dto import EventDto
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
    user_id: int
    id_event: int
    date: str
    eventname: str = Field(..., max_length=15)
    commment: str


class EventResponse(BaseModel):
    date: str
    eventname: str = Field(..., max_length=15)
    commment: str
    id_event: int

    @classmethod
    def dto_to_response_model(cls, dto_event: EventDto):
        return EventResponse(
            id_event=dto_event.id_event,
            eventname=dto_event.eventname,
            commment=dto_event.comment,
            date=dto_event.date,
        )


class DeletedEventResponce(BaseModel):
    message: str
