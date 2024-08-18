import jwt
from typing import Annotated
from fastapi import HTTPException, Request, Depends
from fastapi import Header, HTTPException
from fastapi.security import HTTPBearer
from schemas.user import UserPayload
from config import settings

auth_scheme = HTTPBearer()

async def get_user_from_token(
    request: Request
) -> UserPayload:
    auth_header_value = request.headers.get("Authorization")
    if auth_header_value is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    _, token_data = auth_header_value.split()
    token_return = UserPayload(**jwt.decode(token_data, settings.auth_secret, algorithms="HS256"))
    return token_return
