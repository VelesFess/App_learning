from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
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


async def get_user_from_token(
    request: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)]
) -> UserOut:
    token = request.headers.get("Authorisation")
    token_return = UserOut(**token.decode)
    return token_return
