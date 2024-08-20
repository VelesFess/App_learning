from config import settings
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.pg_dsn, echo=True)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async_session = async_sessionmaker(engine, expire_on_commit=False)
