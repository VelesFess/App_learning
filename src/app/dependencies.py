from datetime import datetime

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

from config import settings
from schemas.user import UserPayload

auth_scheme = HTTPBearer()


async def get_user_from_token(request: Request) -> UserPayload:
    auth_header_value = request.headers.get("Authorization")
    if auth_header_value is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    _, token_data = auth_header_value.split()
    try:
        token_return = UserPayload(
            **jwt.decode(token_data, settings.auth_secret, algorithms="HS256")
        )
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=400, detail="Token error")
    return token_return


async def date_valid(date: str) -> datetime:
    try:
        return datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=415, detail='Wrong date format "YYYY-MM-DD " expected'
        )
