from db.db import  async_session as  session_pg , engine, Base
from fastapi import FastAPI 
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
Base.metadata.create_all(bind=engine)

def get_db():
    db = session_pg()
    try:
        yield db
    finally:
        db.close()



app = FastAPI(
    title="Calendar",
    description=description,
    summary="Calendar for managing your shedule",
    version="0.0.1",
    )
app.include_router(router1, tags=['Items'])
app.include_router(router_users)


# настроечные подключения
