from db.db import engine as engine_pg
from fastapi import FastAPI
from routers.router1 import router as router1
from routers.users import router as router_users

engine_pg()
app = FastAPI()
app.include_router(router1)
app.include_router(router_users)

# from routers.router1 import router as router1
# app.include_router(router1)
# REST server почитать
# middlewar
# настроечные подключения
# to do  connect swagger
