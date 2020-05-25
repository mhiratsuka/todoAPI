from app.api.models import TodoSchema
from app.db import todos, database

async def post(payload: TodoSchema):
    query = todos.insert().values(title=payload.title, description=payload.description)
    return await database.execute(query=query)

async def get(id: int):
    query = todos.select().where(id == todos.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = todos.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload: TodoSchema):
    query = (
        todos
        .update()
        .where(id == todos.c.id)
        .values(title=payload.title, description=payload.description)
        .returning(todos.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = todos.delete().where(id == todos.c.id)
    return await database.execute(query=query)