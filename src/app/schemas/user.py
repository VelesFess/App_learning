from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserPayload(BaseModel):
    username: str
    email: EmailStr
    authorization: bool

class JwtMessage(BaseModel):
    header: str
    payload: str
    verify_signature: str
