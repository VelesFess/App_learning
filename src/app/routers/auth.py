import jwt
from fastapi import APIRouter, HTTPException
from schemas.auth import TokenRequest, TokenResponse
from schemas.user import UserPayload
from db.repositories.users.user_repository import UserRepository
from db.dto.users import UserDto
from db.db import async_session
from auth.password_encryptor import PasswordEncryptor
from db.repositories.exceptions import NoRowsFoundError
from config import settings


router = APIRouter()


@router.post("/auth", tags=["auth"], response_model=TokenResponse)
async def auth_user(
    data: TokenRequest,
):
    # Fetching user from DB
    try:
        async with async_session() as session:
            user: UserDto = await UserRepository.get_user_by_login(
                session,
                login=data.login
            )
    except NoRowsFoundError as e:
        raise HTTPException(status_code=401, detail="User with such login not found!") from e
    # Checking password
    if not PasswordEncryptor.check(data.password, user.password):
        raise HTTPException(status_code=401, detail="Passwords does not match!")
    # Generating token and response
    token = jwt.encode(
        UserPayload(
            login=user.login,
            email=user.email,
            name=user.name,
            id=user.id,
        ).dict(),
        settings.auth_secret
    )
    return TokenResponse(
        token=token,
        login=user.login,
        user_id=user.id
    )
