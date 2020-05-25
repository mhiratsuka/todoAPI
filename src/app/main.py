from app.api import todos, hello
from app.db import engine, metadata, database
from fastapi import FastAPI

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(hello.router)
app.include_router(todos.router, prefix="/todos", tags=["todos"])
