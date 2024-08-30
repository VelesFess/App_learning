from datetime import datetime

from pydantic import BaseModel, BeforeValidator, Field, ValidationError
from typing_extensions import Annotated


def check_date(date: str):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except Exception:
        raise ValidationError


class BaseEventDto(BaseModel):
    user_id: int
    eventname: str = Field(..., max_length=15)
    comment: str
    date: Annotated[str, BeforeValidator(check_date)]


class CreateEventDto(BaseEventDto):
    pass


class EventDto(BaseEventDto):
    id_event: int
