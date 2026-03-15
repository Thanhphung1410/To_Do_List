from typing import Optional

from sqlmodel import Session

from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import Todo, TodoCreate, TodoPatch, TodoUpdate


class TodoService:
    def __init__(self, session: Session) -> None:
        self.repo = TodoRepository(session)

    def create(self, data: TodoCreate) -> Todo:
        return self.repo.create(data)

    def get(self, todo_id: int) -> Optional[Todo]:
        return self.repo.get(todo_id)

    def update(self, todo: Todo, data: TodoUpdate) -> Todo:
        return self.repo.update(todo, data)

    def patch(self, todo: Todo, data: TodoPatch) -> Todo:
        return self.repo.patch(todo, data)

    def delete(self, todo: Todo) -> None:
        self.repo.delete(todo)

    def list(
        self,
        *,
        is_done: Optional[bool],
        q: Optional[str],
        sort: Optional[str],
        limit: int,
        offset: int,
    ) -> tuple[list[Todo], int]:
        return self.repo.list(is_done=is_done, q=q, sort=sort, limit=limit, offset=offset)

    def complete(self, todo: Todo) -> Todo:
        patch = TodoPatch(is_done=True)
        return self.repo.patch(todo, patch)
