from db.dto.event_dto import CreateEventDto, EventDto
from db.models.event_table import Event
from db.repositories.exceptions import NoRowsFoundError
from schemas.event import EventResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import BooleanClauseList


class EventRepository:
    @classmethod
    def db_model_to_dto(cls, db_event: Event) -> EventDto:
        return EventDto(
            login=db_event.login,
            username = db_event.username,
            eventname = db_event.username,
            comment=db_event.comment,
            date=db_event.date,
            id = db_event.id,
        )

    @classmethod
    def dto_to_response_model(cls, dto_event: EventDto) -> EventResponse:
        return EventResponse(
            login=dto_event.login,
            eventname=dto_event.username,
            id=dto_event.id,
            commment=dto_event.comment , 
            date=dto_event.date,
        )

    @classmethod
    async def get_event(cls, db: AsyncSession, event_id: int, username: str) -> EventDto:
        event_list = await cls.get_events(
            db, filters = [Event.id == event_id, Event.username == username], limit=1
        )
        if len(event_list) == 0:
            raise NoRowsFoundError(f"Event for {username} with {event_id=} not found")
        return event_list[0]

 
    @classmethod
    async def get_event_by_date(
        cls, db: AsyncSession, date: str, username:str
    ) -> EventDto:
        event_list = await cls.get_events(
            db, filters= [Event.date == date, Event.username == username], limit=1
        )
        if len(event_list) == 0:
            raise NoRowsFoundError(f"Event for {username} with {date=} not found")
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
            login=event.login,
            username=event.username,
            date = event.date,
            eventname = event.eventname,
            comment = event.date,
        )
        db.add(db_event)
        await db.commit()
        await db.refresh(db_event)
        return cls.db_model_to_dto(db_event)