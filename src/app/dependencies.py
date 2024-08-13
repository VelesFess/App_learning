import jwt
from typing import Annotated
from fastapi import HTTPException, Request
from fastapi import Header, HTTPException
from fastapi.security import HTTPBearer
from schemas.user import UserPayload


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(
            status_code=400, detail="No Jessica token provided"
        )  # noqa: E501
    
    # зависимость для понга - get_user_from_token  Request:request ->
#  request.Header.get('Authorisation')->token -> token.decode

auth_scheme = HTTPBearer()

async def get_user_from_token(
    request: Annotated[Request, auth_scheme]
) -> UserPayload:
    auth_header_value = request.headers.get("Authorization")
    if auth_header_value is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    _, token_data = auth_header_value.split()
    token_return = UserPayload(**jwt.decode(token_data))
    return token_return
