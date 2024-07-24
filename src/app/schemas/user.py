from pydantic import BaseModel, EmailStr
from fastapi import  Request, Header
from typing import Annotated
from fastapi.security import  HTTPBearer


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


# зависимость для понга - get_user_from_token  Request:request -. request.Header.get('Authorisation')->token -> token.decode 

auth_scheme = HTTPBearer()
async def get_user_from_token(request:  Annotated[Request, Header()]) -> UserOut: 
    token=request.Header.get('Authorisation')
    token_return=UserOut(**token.decode)
    return token_return
