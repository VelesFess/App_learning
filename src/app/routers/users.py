from auth.password_encryptor import PasswordEncryptor
from db.db_build import async_session
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


@router.post("/ping")
async def pong(user: UserPayload = Depends(get_user_from_token)):
    return {"ping": f"pong, {user.login}!"}


@router.get("/users/me", tags=["users"], response_model=UserResponse)
async def get_me_as_user(user: UserPayload = Depends(get_user_from_token)):
    pre_response = UserRepository.get_user_by_login(
        async_session, UserPayload.login
    )
    return UserRepository.dto_to_response_model(pre_response)


@router.get("/users/{username}", tags=["users"], response_model=UserResponse)
async def get_other_user(
    username: str, user: UserPayload = Depends(get_user_from_token)
):
    pre_response = UserRepository.get_user_by_username(async_session, username)
    return UserRepository.dto_to_response_model(pre_response)
