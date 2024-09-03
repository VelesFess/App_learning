from datetime import datetime

from db.db_build import async_session
from db.dto.event_dto import CreateEventDto, EventDto
from db.repositories.events.event_repository import EventRepository
from dependencies import get_user_from_token
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from schemas.event import (
    CreateEventPayload,
    DeletedEventResponce,
    EventResponse,
)
from schemas.user import UserPayload

router = APIRouter(dependencies=[Depends(HTTPBearer())])


@router.get("/events/", tags=["events"], response_model=list[EventResponse])
async def read_events(
    event_date: str | None = None,
    user: UserPayload = Depends(get_user_from_token),
):
    return await EventRepository.read_events(user, event_date)


@router.post(
    "/events/", tags=["events"], response_model=EventResponse, status_code=201
)
async def create_event(
    create_event_payload: CreateEventPayload,
    user: UserPayload = Depends(get_user_from_token),
):
    try:
        datetime.strptime(create_event_payload.date, "%Y-%m-%d")
    except Exception:
        raise HTTPException(
            status_code=415, detail='Wrong date format "YYYY-MM-DD " expected'
        )

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
        eventname=event.eventname,
        comment=event.comment,
        date=event.date,
        id_event=event.id_event,
    )


@router.get(
    "/events/{id_event}", tags=["events"], response_model=EventResponse
)
async def get_event_by_id(
    event_id: int, user: UserPayload = Depends(get_user_from_token)
):
    pre_response = EventRepository.get_event(
        async_session, event_id, UserPayload.name
    )
    return EventResponse.dto_to_response_model(pre_response)


@router.delete(
    "/events/{id_event}",
    tags=["events"],
    response_model=DeletedEventResponce,
    status_code=201,
)
async def delete_event_by_id(
    event_id: int, user: UserPayload = Depends(get_user_from_token)
):
    EventRepository.delete_event(async_session, event_id)
    return DeletedEventResponce(message="Event deleted successfully")
