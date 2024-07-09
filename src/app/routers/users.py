from fastapi import APIRouter
from schemes.auth import TokenRequest, TokenResponse

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
