import jwt
from config import settings
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
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
        raise HTTPException(status_code=400, detail="token error")
    return token_return
