from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import BooleanClauseList

from db.dto.users import CreateUserDto, UserDto
from db.models.users import User
from db.repositories.exceptions import NoRowsFoundError


class UserRepository:
    @classmethod
    def db_model_to_dto(cls, db_user: User) -> UserDto:
        return UserDto(
            login=db_user.login,
            name=db_user.name,
            email=db_user.email,
            password=db_user.password,
            id=db_user.id,
        )

    @classmethod
    async def get_user(cls, db: AsyncSession, user_id: int) -> UserDto:
        user_list = await cls.get_users(db, filters=User.id == user_id, limit=1)
        if len(user_list) == 0:
            raise NoRowsFoundError(f"User with {user_id=} not found")
        return user_list[0]

    @classmethod
    async def get_user_by_email(cls, db: AsyncSession, email: str) -> UserDto:
        user_list = await cls.get_users(db, filters=User.email == email, limit=1)
        if len(user_list) == 0:
            raise NoRowsFoundError(f"User with {email=} not found")
        return user_list[0]

    @classmethod
    async def get_user_by_username(cls, db: AsyncSession, username: str) -> UserDto:
        user_list = await cls.get_users(db, filters=User.name == username, limit=1)
        if len(user_list) == 0:
            raise NoRowsFoundError(f"User with {username=} not found")
        return user_list[0]

    @classmethod
    async def get_user_by_login(cls, db: AsyncSession, login: str) -> UserDto:
        user_list = await cls.get_users(db, filters=User.login == login, limit=1)
        if len(user_list) == 0:
            raise NoRowsFoundError(f"User with {login=} not found")
        return user_list[0]

    @classmethod
    async def get_users(
        cls,
        db: AsyncSession,
        filters: BooleanClauseList | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> UserDto:
        query = select(User)
        if filters:
            query = query.where(filters)
        query = query.offset(skip).limit(limit)
        query_result = await db.execute(query)
        return [cls.db_model_to_dto(user) for user, in query_result.all()]

    @classmethod
    async def create_user(cls, db: AsyncSession, user: CreateUserDto) -> UserDto:
        db_user = User(
            login=user.login,
            name=user.name,
            email=user.email,
            password=user.password,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return cls.db_model_to_dto(db_user)
