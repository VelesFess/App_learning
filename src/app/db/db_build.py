from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings

engine = create_async_engine(settings.pg_dsn, echo=True)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async_session = async_sessionmaker(engine, expire_on_commit=False)


def get_sessionmaker():
    return async_session
