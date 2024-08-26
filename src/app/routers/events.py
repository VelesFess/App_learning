from db.db_build import async_session
from db.dto.event_dto import CreateEventDto, EventDto
from db.repositories.events.event_repository import EventRepository
from dependencies import get_user_from_token
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from schemas.event import CreateEventPayload, EventResponse, EventPayload, DeletedEventResponce
from schemas.user import UserPayload
from db.models.event_table import Event
from sqlalchemy.sql.elements import BooleanClauseList

router = APIRouter(dependencies=[Depends(HTTPBearer())])


@router.get("/events/", tags=["events"], response_model=list[EventResponse])
async def read_events(event_date:str, user: UserPayload = Depends(get_user_from_token)):
    filters_temp : BooleanClauseList = [user.name == Event.username]
    if event_date:
        filters_temp=filters_temp._append_inplace(event_date == Event.date)
    async with async_session() as session:
        events: list[EventDto] = await EventRepository.get_events(session, filters = filters_temp)
    return [
        EventResponse.dto_to_response_model(event)
        for event in events
    ]


@router.post("/events/", tags=["events"], response_model=EventResponse,status_code=201)
async def create_event(create_event_payload: CreateEventPayload, user: UserPayload = Depends(get_user_from_token)):
    async with async_session() as session:
        event: EventDto = await EventRepository.create_event(
            session,
            CreateEventDto(
                login=create_event_payload.login,
                username=create_event_payload.username,
                eventname=create_event_payload.eventname,
                comment=create_event_payload.comment,
                date=create_event_payload.date,
            ),
        )
    return EventResponse(
        login=event.login,
        username=event.username,
        eventname=event.eventname,
        comment=event.comment,
        date=event.date,
        id=event.id
    )


@router.get("/events/{id_event}", tags=["events"], response_model=EventResponse)
async def get_event_by_id( event_id: int ,user: UserPayload = Depends(get_user_from_token)):
    pre_response = EventRepository.get_event(
        async_session, event_id, UserPayload.name
    )
    return EventResponse.dto_to_response_model(pre_response)


@router.delete("/events/{id_event}", tags=["events"], response_model=DeletedEventResponce)
async def delete_event_by_id(event:EventPayload, user: UserPayload = Depends(get_user_from_token)):
    pre_response = EventRepository.delete_event(
        async_session, event
    )
    return  DeletedEventResponce(message=f"Event deleted successfully")