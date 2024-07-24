import jwt
from fastapi import APIRouter ,HTTPException, Depends
from pydantic import ValidationError
from schemas.user import  UserPayload , get_user_from_token

from schemas.auth import TokenRequest, TokenResponse
from typing import Annotated
from jwt.exceptions import InvalidTokenError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
auth_scheme = HTTPBearer()

async def verify_key(token:  Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)]) -> UserPayload: 
    try:
        user_payload=jwt.decode(token, "secret", algorithms=["HS256"])
    except InvalidTokenError:
        print('Error from 40str')
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        result=UserPayload(**user_payload) # распаковка объекта через kwargs 
        # result=UserPayload(id=user_payload["id"],username=user_payload["username"],)
    except ValidationError:
        raise HTTPException(status_code=500, detail=ValidationError.errors) 
    return result




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


@router.post("/ping", dependencies=[Depends(verify_key)])
async def pong():
    return {"ping": "pong!"}

# Глобольная депенденси()
# зависимость для понга - get_user_from_token  Request:request -. request.Header.get('Authorisation')->token -> token.decode 