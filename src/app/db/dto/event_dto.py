from pydantic import BaseModel, Field, ValidationError, BeforeValidator
from typing_extensions import Annotated
from datetime import datetime


def check_date(date:str):
    try :
        return datetime.strptime(date,'%Y-%m-%d')
    except:
        raise ValidationError


class BaseEventDto(BaseModel):
    user_id : int
    eventname: str = Field(..., max_length=15)
    comment: str
    date: Annotated[str,BeforeValidator(check_date)]


class CreateEventDto(BaseEventDto):
    pass


class EventDto(BaseEventDto):
    id_event: int
