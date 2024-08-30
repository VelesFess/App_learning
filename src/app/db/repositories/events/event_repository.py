from datetime import datetime

from db.db_build import async_session
from db.dto.event_dto import CreateEventDto, EventDto
from db.models.event_table import Event
from db.repositories.exceptions import NoRowsFoundError
from fastapi import HTTPException
from schemas.event import EventResponse
from schemas.user import UserPayload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import BooleanClauseList


def check_date(date: str):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except Exception:
        raise HTTPException(
            status_code=415, detail='Wrong date format "YYYY-MM-DD " expected'
        )


class EventRepository:
    @classmethod
    def db_model_to_dto(cls, db_event: Event) -> EventDto:
        return EventDto(
            user_id=db_event.user_id,
            eventname=db_event.eventname,
            comment=db_event.comment,
            date=db_event.date,
            id_event=db_event.id,
        )

    @classmethod
    async def get_event(
        cls, db: AsyncSession, event_id: int, user_id: int
    ) -> EventDto:
        event_list = await cls.get_events(
            db,
            filters=[Event.id_event == event_id, Event.user_id == user_id],
            limit=1,
        )
        if len(event_list) == 0:
            raise NoRowsFoundError(
                f"Event for user {user_id=} with {event_id=} not found"
            )
        return event_list[0]

    @classmethod
    async def get_event_by_date(
        cls, db: AsyncSession, date: str, user_id: int
    ) -> EventDto:
        event_list = await cls.get_events(
            db, filters=[Event.date == date, Event.user_id == user_id], limit=1
        )
        if len(event_list) == 0:
            raise NoRowsFoundError(
                f"Event for user {user_id=} with {date=} not found"
            )
        return event_list[0]

    @classmethod
    async def get_events(
        cls,
        db: AsyncSession,
        filters: BooleanClauseList | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> EventDto:
        query = select(Event)
        if filters:
            query = query.where(filters)
        query = query.offset(skip).limit(limit)
        query_result = await db.execute(query)
        return [cls.db_model_to_dto(event) for event, in query_result.all()]

    @classmethod
    async def create_event(
        cls, db: AsyncSession, event: CreateEventDto
    ) -> EventDto:
        db_event = Event(
            user_id=event.user_id,
            date=event.date,
            eventname=event.eventname,
            comment=event.date,
        )
        db.add(db_event)
        await db.commit()
        await db.refresh(db_event)
        return cls.db_model_to_dto(db_event)

    @classmethod
    async def delete_event(cls, db: AsyncSession, event_id: int):
        query = select(Event)
        query = query.where(id == event_id)
        if not query:
            raise NoRowsFoundError(f"Event for  with {id=} not found")
        db.delete(query)
        await db.commit()

    @classmethod
    async def read_events(
        user: UserPayload,
        event_date: str | None = None,
        eventname: str | None = None,
        comment: str | None = None,
    ):
        filters_temp: BooleanClauseList = [user.id == Event.user_id]
        if event_date:
            filters_temp = filters_temp._append_inplace(
                event_date == Event.date
            )
        if eventname:
            filters_temp = filters_temp._append_inplace(
                eventname == Event.eventname
            )
        if comment:
            filters_temp = filters_temp._append_inplace(
                comment == Event.comment
            )
        async with async_session() as session:
            events: list[EventDto] = await EventRepository.get_events(
                session, filters=filters_temp
            )
        return [EventResponse.dto_to_response_model(event) for event in events]
