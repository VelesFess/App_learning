from pydantic import BaseModel, EmailStr


class CreateUserPayload(BaseModel):
    login: str
    name: str
    email: EmailStr
    password: str


class UserPayload(BaseModel):
    login: str
    email: EmailStr
    name: str
    id: int


class UserResponse(BaseModel):
    login: str
    name: str
    email: EmailStr
    id: int
