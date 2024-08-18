from auth.password_encryptor import PasswordEncryptor
from db.db import async_session
from db.dto.users import CreateUserDto, UserDto
from db.repositories.users.user_repository import UserRepository
from dependencies import get_user_from_token
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from schemas.user import CreateUserPayload, UserPayload, UserResponse

router = APIRouter(dependencies=[Depends(HTTPBearer())])


@router.get("/users/", tags=["users"], response_model=list[UserResponse])
async def read_users():
    async with async_session() as session:
        users: list[UserDto] = await UserRepository.get_users(session)
    return [
        UserResponse(
            login=user.login, name=user.name, email=user.email, id=user.id
        )
        for user in users
    ]


@router.post("/users/", tags=["users"], response_model=UserResponse)
async def create_user(create_user_payload: CreateUserPayload):
    async with async_session() as session:
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


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}


@router.post("/ping")
async def pong(user: UserPayload = Depends(get_user_from_token)):
    return {"ping": f"pong, {user.login}!"}


@router.post("/users/me")
async def get_me_as_user(user: UserPayload = Depends(get_user_from_token)):
    return UserRepository.get_user_by_login(async_session, UserPayload.login)


@router.post("/users/{username}")
async def get_other_user(
    username: str, user: UserPayload = Depends(get_user_from_token)
):
    return UserRepository.get_user_by_username(async_session, username)
