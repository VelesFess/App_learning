from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from schemas.user import UserResponse, UserPayload, CreateUserPayload
from db.repositories.users.user_repository import UserRepository
from db.dto.users import CreateUserDto, UserDto
from db.db import async_session
from dependencies import get_user_from_token
from auth.password_encryptor import PasswordEncryptor


router = APIRouter(
    dependencies=[Depends(HTTPBearer())]
)


@router.get("/users/", tags=["users"], response_model=list[UserResponse])
async def read_users():
    async with async_session() as session:
        users: list[UserDto] = await UserRepository.get_users(session)
    return [
        UserResponse(
            login=user.login,
            name=user.name,
            email=user.email,
            id=user.id
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
                )
            )
        )
    return UserResponse(
        login=user.login,
        name=user.name,
        email=user.email,
        id=user.id
    )


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}


@router.post("/ping")
async def pong(
    user: UserPayload = Depends(get_user_from_token)
):
    return {"ping": f"pong, {user.login}!"}
