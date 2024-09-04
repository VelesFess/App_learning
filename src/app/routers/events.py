from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from db.db_build import get_sessionmaker
from db.dto.event_dto import CreateEventDto, EventDto
from db.repositories.events.event_repository import EventRepository
from dependencies import date_valid, get_user_from_token
from schemas.event import CreateEventPayload, DeletedEventResponce, EventResponse
from schemas.user import UserPayload

router = APIRouter(dependencies=[Depends(HTTPBearer())])


@router.get("/events/", tags=["events"], response_model=list[EventResponse])
async def read_events(
    event_date: Annotated[str | None, Depends(date_valid)] = None,
    user: UserPayload = Depends(get_user_from_token),
    async_session=Depends(get_sessionmaker),
):
    events: list[EventDto] = await EventRepository.read_events(user, event_date)
    return [EventResponse(event) for event in events]


@router.post("/events/", tags=["events"], response_model=EventResponse, status_code=201)
async def create_event(
    create_event_payload: CreateEventPayload,
    user: UserPayload = Depends(get_user_from_token),
    async_session=Depends(get_sessionmaker),
):
    async with async_session() as session:
        event: EventDto = await EventRepository.create_event(
            session,
            CreateEventDto(
                user_id=user.id,
                eventname=create_event_payload.eventname,
                comment=create_event_payload.comment,
                date=date_valid(create_event_payload.date),
            ),
        )

    return EventResponse(
        eventname=event.eventname,
        comment=event.comment,
        date=event.date,
        id_event=event.id_event,
    )


@router.get("/events/{id_event}", tags=["events"], response_model=EventResponse)
async def get_event_by_id(
    event_id: int,
    user: UserPayload = Depends(get_user_from_token),
    async_session=Depends(get_sessionmaker),
):
    pre_response: EventDto = EventRepository.get_event(
        async_session, event_id, UserPayload.name
    )
    return EventResponse(
        id_event=pre_response.id_event,
        eventname=pre_response.eventname,
        commment=pre_response.comment,
        date=pre_response.date,
    )


@router.delete(
    "/events/{id_event}",
    tags=["events"],
    response_model=DeletedEventResponce,
    status_code=201,
)
async def delete_event_by_id(
    event_id: int,
    user: UserPayload = Depends(get_user_from_token),
    async_session=Depends(get_sessionmaker),
):
    EventRepository.delete_event(async_session, event_id)
    return DeletedEventResponce(message="Event deleted successfully")
