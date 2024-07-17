from db.db import  async_session as  session_pg
from fastapi import FastAPI
from routers.router1 import router as router1
from routers.users import router as router_users


session_pg()
app = FastAPI()
app.include_router(router1, tags=['Items'])
app.include_router(router_users)

# REST server почитать
# middlewar
# настроечные подключения
