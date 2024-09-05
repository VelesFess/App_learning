import jwt
from fastapi import APIRouter, Depends, HTTPException

from auth.password_encryptor import PasswordEncryptor
from config import settings
from db.db_build import get_sessionmaker
from db.dto.users import UserDto
from db.repositories.exceptions import NoRowsFoundError
from db.repositories.users.user_repository import UserRepository
from schemas.auth import TokenRequest, TokenResponse
from schemas.user import UserPayload

router = APIRouter()


@router.post("/auth", tags=["auth"], response_model=TokenResponse)
async def auth_user(
    data: TokenRequest,
    async_session=Depends(get_sessionmaker),
):
    # Fetching user from DB
    try:
        async with async_session() as session:
            user: UserDto = await UserRepository.get_user_by_login(
                session, login=data.login
            )
    except NoRowsFoundError as e:
        raise HTTPException(
            status_code=401, detail="User with such login not found!"
        ) from e
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
        settings.auth_secret,
    )
    return TokenResponse(token=token, login=user.login, user_id=user.id)
