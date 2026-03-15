from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.core.database import engine
from app.schemas.todo import (
    TodoCreate,
    TodoListResponse,
    TodoPatch,
    TodoRead,
    TodoUpdate,
)
from app.services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["todos"])


def get_session():
    with Session(engine) as session:
        yield session


def get_service(session: Session = Depends(get_session)) -> TodoService:
    return TodoService(session)


@router.post("", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, service: TodoService = Depends(get_service)):
    return service.create(payload)


@router.get("", response_model=TodoListResponse)
def list_todos(
    service: TodoService = Depends(get_service),
    is_done: Optional[bool] = Query(default=None),
    q: Optional[str] = Query(default=None, min_length=1),
    sort: Optional[str] = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    items, total = service.list(is_done=is_done, q=q, sort=sort, limit=limit, offset=offset)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/{todo_id}", response_model=TodoRead)
def get_todo(todo_id: int, service: TodoService = Depends(get_service)):
    todo = service.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: int, payload: TodoUpdate, service: TodoService = Depends(get_service)
):
    todo = service.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return service.update(todo, payload)


@router.patch("/{todo_id}", response_model=TodoRead)
def patch_todo(
    todo_id: int, payload: TodoPatch, service: TodoService = Depends(get_service)
):
    todo = service.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return service.patch(todo, payload)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, service: TodoService = Depends(get_service)):
    todo = service.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    service.delete(todo)
    return None


@router.post("/{todo_id}/complete", response_model=TodoRead)
def complete_todo(todo_id: int, service: TodoService = Depends(get_service)):
    todo = service.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return service.complete(todo)
