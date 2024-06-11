from fastapi import FastAPI

# from routers.router import router as router1

app = FastAPI()


# app.include_router(router1)
# REST server почитать
# to do  connect swagger
@app.get("/ping")
def pong():
    return {"ping": "pong!"}
