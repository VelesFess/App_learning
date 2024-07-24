from typing import Annotated

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPayload(BaseModel):
    username: str
    id: int


class JwtMessage(BaseModel):
    header: str
    payload: str
    verify_signature: str


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None


# зависимость для понга - get_user_from_token  Request:request ->
#  request.Header.get('Authorisation')->token -> token.decode

auth_scheme = HTTPBearer()


async def get_user_from_token(request: Annotated[Request, auth_scheme]) -> UserOut:
    token = request.headers.get("Authorisation")
    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token_return = UserOut(**token.decode)
    return token_return
