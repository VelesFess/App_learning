import jwt
from fastapi import APIRouter ,HTTPException, Header
from pydantic import EmailStr , ValidationError
from schemas.user import CreateUser, UserPayload, JwtMessage
from schemas.auth import TokenRequest, TokenResponse
from typing import Annotated
from jwt.exceptions import InvalidTokenError

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}


@router.post("/auth", tags=["users"], response_model=TokenResponse)
async def auth_user(
    data: TokenRequest,
    # user_repository: UserRepository = Depends(func_to_get_user_repository)
):
    return "jwt"


async def verify_key(user_data: Annotated[str, Header(alias='authorization')]):
    try:
        user_payload=jwt.decode(user_data, "secret", algorithms=["HS256"])
    except InvalidTokenError:
        raise HTTPException(status_code=400, detail="Unauthorized")
    if  user_payload['authorization'] != True:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        user_payload.model_validate({'authorization': 'True'})
    except:
        raise HTTPException(status_code=501, detail=ValidationError.errors) 
    return user_payload


@router.post("/ping")
async def pong(user_data: Annotated[str, verify_key]):
    return {"ping": "pong!"}