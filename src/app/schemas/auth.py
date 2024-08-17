from pydantic import BaseModel


class TokenResponse(BaseModel):
    token: str
    login: str
    user_id: int


class TokenRequest(BaseModel):
    login: str
    password: str
