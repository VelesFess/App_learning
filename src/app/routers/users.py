from typing import Annotated
import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from schemas.auth import TokenRequest, TokenResponse
from schemas.user import UserResponse, UserPayload, CreateUserPayload
from db.repositories.users.user_repository import UserRepository
from db.dto.users import CreateUserDto, UserDto
from db.db import async_session
from dependencies import get_user_from_token


router = APIRouter()
auth_scheme = HTTPBearer()


async def verify_key(
    token: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)]
) -> UserPayload:
    try:
        user_payload = jwt.decode(token, "secret", algorithms=["HS256"])
    except InvalidTokenError:
        print("Error from 40str")
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        result = UserPayload(**user_payload)  # распаковка объекта через kwargs
        # result=UserPayload(id=user_payload["id"],username=user_payload["username"],)
    except ValidationError:
        raise HTTPException(status_code=500, detail=ValidationError.errors)
    return result


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
                password=create_user_payload.password
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


@router.post("/auth", tags=["users"], response_model=TokenResponse)
async def auth_user(
    data: TokenRequest,
):
    return "jwt"


@router.post("/ping", dependencies=[Depends(get_user_from_token)])
async def pong():
    return {"ping": "pong!"}


# Глобольная депенденси()
# зависимость для понга - get_user_from_token  Request:request ->
# request.Header.get('Authorisation')->token -> token.decode
