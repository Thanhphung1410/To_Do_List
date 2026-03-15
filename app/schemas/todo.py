from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class TodoBase(SQLModel):
    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: bool = False


class Todo(TodoBase, table=True):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )
    )


class TodoCreate(TodoBase):
    pass


class TodoUpdate(SQLModel):
    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: bool = False


class TodoPatch(SQLModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: Optional[bool] = None


class TodoRead(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime


class TodoListResponse(SQLModel):
    items: list[TodoRead]
    total: int
    limit: int
    offset: int
