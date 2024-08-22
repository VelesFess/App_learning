from contextlib import asynccontextmanager

from db.db_build import Base, engine
from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.router1 import router as router1
from routers.users import router as router_users

description = """
Calendar API helps you with managing your shedule. 🚀


## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
* **Create event** (_not implemented_).
"""


# @asynccontextmanager
# async def DB(app: FastAPI):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata)
#     await engine.dispose()


app = FastAPI(
    title="Calendar",
    description=description,
    summary="Calendar for managing your shedule",
    version="0.0.1",
    # lifespan=DB,
)

app.include_router(router1, tags=["Items"])
app.include_router(router_users)
app.include_router(auth_router)


# события ()
# добавитьь функцию списка событий по пользователю /events/ @get       user_id из токена # noqa: E501
# добавления события /events/   @post
# удаления события /events/{id_event} @ delete
# получения события /events/{id_event} @get
# получения события на дату /events/?date={event_date} @get
#  дата пользователь(форм кей ) id (праймари) название(ограничить по длине ) коментарий # noqa: E501

# event_date format = YYYY-mm-dd
