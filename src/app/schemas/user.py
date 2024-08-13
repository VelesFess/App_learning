from pydantic import BaseModel, EmailStr

# Очень много повторяющихся схем, нужно переиспользовать модели
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


# class JwtMessage(BaseModel):
#     header: str
#     payload: str
#     verify_signature: str


# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: str | None = None


# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None


# class UserInDB(BaseModel):
#     username: str
#     hashed_password: str
#     email: EmailStr
#     full_name: str | None = None

class UserResponse(BaseModel):
    login: str
    name: str
    email: EmailStr
    id: int
