import asyncio
import typing

import jwt
import pytest
from auth.password_encryptor import PasswordEncryptor
from config import settings
from db.db_build import engine, get_sessionmaker
from db.dto.users import CreateUserDto, UserDto
from db.repositories.users.user_repository import UserRepository
from fastapi import FastAPI
from httpx import AsyncClient
from main import app
from schemas.user import UserPayload
from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import AsyncSession


class DependencyOverrider:
    def __init__(
        self,
        app: FastAPI,
        overrides: typing.Mapping[typing.Callable, typing.Callable],
    ) -> None:
        self.overrides = overrides
        self._app = app
        self._old_overrides: dict = {}

    def __enter__(self):
        for dep, new_dep in self.overrides.items():
            if dep in self._app.dependency_overrides:
                # Save existing overrides
                self._old_overrides[dep] = self._app.dependency_overrides[dep]
            self._app.dependency_overrides[dep] = new_dep
        return self

    def __exit__(self, *args: typing.Any) -> None:
        for dep in self.overrides.keys():
            if dep in self._old_overrides:
                # Restore previous overrides
                self._app.dependency_overrides[dep] = self._old_overrides.pop(
                    dep
                )
            else:
                # Just delete the entry
                del self._app.dependency_overrides[dep]


@pytest.yield_fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def async_db_session(event_loop):
    async with engine.connect() as conn:
        await conn.begin()

        # note this points to the sync version of the Transaction
        nested = (await conn.begin_nested()).sync_transaction

        async_session = AsyncSession(conn)

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session, transaction):
            nonlocal nested
            # inside the event, we deal with the sync version of the
            # connection to make a new nested transaction
            if not nested.is_active and not conn.closed:
                nested = conn.sync_connection.begin_nested()

        class SessionmakerStub:
            def __call__(self):
                return async_session

        # work with AsyncSession here, commit and rollback OK
        # ...

        with DependencyOverrider(
            app, {get_sessionmaker: lambda: SessionmakerStub()}
        ):
            yield async_session

        # rollback outer transaction
        await conn.rollback()


@pytest.fixture(scope="function", autouse="True")
async def setup(async_db_session):
    tables = (
        (
            await async_db_session.execute(
                text(
                    "SELECT table_name FROM information_schema.tables"
                    " WHERE table_schema='public'"
                )
            )
        )
        .scalars()
        .all()
    )
    for tablename in tables:
        await async_db_session.execute(
            text(f"TRUNCATE TABLE {tablename} CASCADE")
        )


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def admin(async_db_session):
    db_user: UserDto = await UserRepository.create_user(
        async_db_session,
        CreateUserDto(
            login="admin",
            name="admin",
            password=PasswordEncryptor.encrypt("admin"),
            email="admin@example.com",
        ),
    )
    return db_user


@pytest.fixture
async def admin_token(admin):
    return jwt.encode(
        UserPayload(
            login=admin.login,
            email=admin.email,
            name=admin.name,
            id=admin.id,
        ).dict(),
        settings.auth_secret,
    )


@pytest.fixture
async def create_test_user(async_db_session):
    db_user: UserDto = await UserRepository.create_user(
        async_db_session,
        CreateUserDto(
            login="string_test",
            name="string_test",
            password=PasswordEncryptor.encrypt("string_test"),
            email="string_test@example.com",
        ),
    )
    return db_user


@pytest.fixture
async def fix_get_test_user_by_username(async_db_session):
    db_user: UserDto = await UserRepository.get_user_by_username(
        async_db_session, "string"
    )
    return db_user


@pytest.fixture
async def user_token(user):
    return jwt.encode(
        UserPayload(
            login=user.login,
            email=user.email,
            name=user.name,
            id=user.id,
        ).dict(),
        settings.auth_secret,
    )
