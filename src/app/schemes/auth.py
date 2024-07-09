from pydantic import BaseModel


class TokenResponse(BaseModel):
    token: str
    username: str
    user_id: int


class TokenRequest(BaseModel):
    login: str
    password: str
