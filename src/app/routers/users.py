from auth.password_encryptor import PasswordEncryptor
from db.db_build import get_sessionmaker
from db.dto.users import CreateUserDto, UserDto
from db.repositories.exceptions import NoRowsFoundError
from db.repositories.users.user_repository import UserRepository
from dependencies import get_user_from_token
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from schemas.user import (
    CreateUserPayload,
    DeletedUserResponce,
    UserPayload,
    UserResponse,
)

router = APIRouter(dependencies=[Depends(HTTPBearer())])


@router.get(
    "/users/",
    tags=["users"],
    response_model=list[UserResponse],
    status_code=200,
)
async def read_users(
    user: UserPayload = Depends(get_user_from_token),
    async_session=Depends(get_sessionmaker),
):
    async with async_session() as session:
        users: list[UserDto] = await UserRepository.get_users(session)
    return [
        UserResponse(
            login=user.login, name=user.name, email=user.email, id=user.id
        )
        for user in users
    ]


@router.post(
    "/users/", tags=["users"], response_model=UserResponse, status_code=201
)
async def create_user(
    create_user_payload: CreateUserPayload,
    async_session=Depends(get_sessionmaker),
):
    async with async_session() as session:
        try:
            await UserRepository.get_user_by_login(
                session, login=create_user_payload.login
            )
            raise HTTPException(status_code=400, detail="User already exist")
        except NoRowsFoundError:
            user: UserDto = await UserRepository.create_user(
                session,
                CreateUserDto(
                    login=create_user_payload.login,
                    name=create_user_payload.name,
                    email=create_user_payload.email,
                    password=PasswordEncryptor.encrypt(
                        create_user_payload.password
                    ),
                ),
            )
    return UserResponse(
        login=user.login, name=user.name, email=user.email, id=user.id
    )


@router.post("/ping")
async def pong(user: UserPayload = Depends(get_user_from_token)):
    return {"ping": f"pong, {user.login}!"}


@router.get("/users/me", tags=["users"], response_model=UserResponse)
async def get_me_as_user(
    user: UserPayload = Depends(get_user_from_token),
    async_session=Depends(get_sessionmaker),
):
    async with async_session() as session:
        pre_response = await UserRepository.get_user_by_login(
            session, user.login
        )
    return UserResponse.dto_to_response_model(pre_response)


@router.get("/users/{username}", tags=["users"], response_model=UserResponse)
async def get_other_user(
    username: str,
    user: UserPayload = Depends(get_user_from_token),
    async_session=Depends(get_sessionmaker),
):
    try:
        async with async_session() as session:
            pre_response = await UserRepository.get_user_by_username(
                session, username
            )
    except NoRowsFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.dto_to_response_model(pre_response)


@router.delete(
    "/users/{username}",
    tags=["users"],
    response_model=DeletedUserResponce,
    status_code=200,
)
async def delete_user_by_login(
    user: UserPayload = Depends(get_user_from_token),
    async_session=Depends(get_sessionmaker),
):
    async with async_session() as session:
        await UserRepository.delete_user(session, user.login)
    return DeletedUserResponce(message="User deleted successfully")
