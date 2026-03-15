from typing import Optional

from sqlmodel import Session, select
from sqlalchemy import func

from app.schemas.todo import Todo, TodoCreate, TodoPatch, TodoUpdate


class TodoRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: TodoCreate) -> Todo:
        todo = Todo.model_validate(data)
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def get(self, todo_id: int) -> Optional[Todo]:
        statement = select(Todo).where(Todo.id == todo_id)
        return self.session.exec(statement).first()

    def update(self, todo: Todo, data: TodoUpdate) -> Todo:
        todo.title = data.title
        todo.description = data.description
        todo.is_done = data.is_done
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def patch(self, todo: Todo, data: TodoPatch) -> Todo:
        if data.title is not None:
            todo.title = data.title
        if data.description is not None:
            todo.description = data.description
        if data.is_done is not None:
            todo.is_done = data.is_done
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def delete(self, todo: Todo) -> None:
        self.session.delete(todo)
        self.session.commit()

    def list(
        self,
        *,
        is_done: Optional[bool],
        q: Optional[str],
        sort: Optional[str],
        limit: int,
        offset: int,
    ) -> tuple[list[Todo], int]:
        statement = select(Todo)

        if is_done is not None:
            statement = statement.where(Todo.is_done == is_done)

        if q:
            keyword = f"%{q.lower()}%"
            statement = statement.where(func.lower(Todo.title).like(keyword))

        total_statement = statement.with_only_columns(func.count()).order_by(None)
        total = self.session.exec(total_statement).one()

        if sort:
            if sort == "created_at":
                statement = statement.order_by(Todo.created_at.asc())
            elif sort == "-created_at":
                statement = statement.order_by(Todo.created_at.desc())
        else:
            statement = statement.order_by(Todo.created_at.desc())

        statement = statement.offset(offset).limit(limit)
        items = self.session.exec(statement).all()
        return items, total
