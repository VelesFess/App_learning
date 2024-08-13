from pydantic import BaseModel, EmailStr


class BaseUserDto(BaseModel):
    login: str
    name: str
    email: EmailStr


class CreateUserDto(BaseUserDto):
    password: str


class UserDto(BaseUserDto):
    id: int
