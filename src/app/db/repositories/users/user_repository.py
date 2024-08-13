# Мы пиешм асинхронный коннектор к БД, тебе нужна асинхронная сессия
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql.elements import BooleanClauseList

# Импорты всегда только абсолютные!!!
# from ....db.models.users import User , UserCreate
from db.models.users import User
from db.repositories.exceptions import NoRowsFoundError
from db.dto.users import CreateUserDto, UserDto


class UserRepository:  # check login & password
    @classmethod
    def db_model_to_dto(cls, db_user: User) -> UserDto:
        return UserDto(
            login=db_user.login,
            name=db_user.name,
            email=db_user.email,
            id=db_user.id
        )

    # Все фунции репозитория не используют его state. По сути здесь класс является инструментом аггрегации функций.
    # Используем декоратор classmethod, чтобы не нужно было инициализировать объект класса
    @classmethod
    async def get_user(cls, db: AsyncSession, user_id: int) -> UserDto:
        # return await db.query(User).filter(User.id == user_id).first()
        user_list = await cls.get_users(filters=User.id == user_id, limit=1)
        if len(user_list) == 0:
            raise NoRowsFoundError(f"User with {user_id=} not found")
        return user_list[0]

    @classmethod
    async def get_user_by_email(cls, db: AsyncSession, email: str) -> UserDto: # check user in db by email
        # return await db.query(User).filter(User.email == email).first()
        user_list = await cls.get_users(filters=User.email == email, limit=1)
        if len(user_list) == 0:
            raise NoRowsFoundError(f"User with {email=} not found")
        return user_list[0]

    @classmethod
    async def get_users(cls, db: AsyncSession, filters: BooleanClauseList | None = None, skip: int = 0, limit: int = 100) -> UserDto:
        # Конструкция Session.query является устаревшей, следует использовать select
        # return await db.query(User).offset(skip).limit(limit).all()
        query = select(User)
        if filters:
            query = query.where(filters)
        query = query.offset(skip).limit(limit)
        query_result = await db.execute(query)
        # У нас архитектура напоминает слоеный пирог. Мы не передаем объекты одного слоя на другой.
        # Для передачи данных следует использовать отдельные DTO (Data Transfer Object)
        return [
            cls.db_model_to_dto(user)
            for user, in query_result.all()
        ]

    @classmethod
    async def create_user(cls, db: AsyncSession, user: CreateUserDto) -> UserDto:
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = User(login=user.login, name=user.name, email=user.email, password=fake_hashed_password)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return cls.db_model_to_dto(db_user)
