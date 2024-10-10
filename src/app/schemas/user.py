from db.dto.users import UserDto
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

    @classmethod
    def dto_to_response_model(cls, dto_user: UserDto):
        return UserResponse(
            login=dto_user.login,
            name=dto_user.name,
            email=dto_user.email,
            id=dto_user.id,
        )


class DeletedUserResponce(BaseModel):
    message: str
