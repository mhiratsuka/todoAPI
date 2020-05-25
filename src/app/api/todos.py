from app.api import crud
from app.api.models import TodoDB, TodoSchema
from fastapi import APIRouter, HTTPException, Path
from typing import List


router = APIRouter()


@router.post("/", response_model=TodoDB, status_code=201)
async def create_todo(payload: TodoSchema):
    todo_id = await crud.post(payload)

    response_object = {
        "id": todo_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.get("/{id}/", response_model=TodoDB)
async def read_todo(id: int = Path(..., gt=0),):
    todo = await crud.get(id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    return todo


@router.get("/", response_model=List[TodoDB])
async def read_all_todos():
    return await crud.get_all()


@router.put("/{id}/", response_model=TodoDB)
async def update_todo(payload: TodoSchema, id: int = Path(..., gt=0),):
    todo = await crud.get(id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    todo_id = await crud.put(id, payload)

    response_object = {
        "id": todo_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.delete("/{id}/", response_model=TodoDB)
async def delete_todo(id: int = Path(..., gt=0)):
    todo = await crud.get(id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    await crud.delete(id)

    return todo



