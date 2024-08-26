from pydantic import BaseModel, EmailStr, Field
from db.dto.event_dto import EventDto


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
    date: str
    eventname: str = Field(..., max_length=15)
    commment: str
    id: int


    @classmethod
    def dto_to_response_model(cls, dto_event: EventDto):
        return EventResponse(
            id=dto_event.id,
            eventname=dto_event.eventname,
            commment=dto_event.comment , 
            date=dto_event.date,
        )
    
class DeletedEventResponce(BaseModel):
    comment:str