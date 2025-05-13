from sqlmodel import Field, SQLModel
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    done = "done"


class Tasks(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, title="ID задачи")
    title: str = Field(index=True, title="Заголовок задачи")
    description: str | None = Field(default=None, title="Описание задачи")
    status: TaskStatus = Field(default=TaskStatus.pending, title="Статус задачи")
    priority: int = Field(default=1, title="Приоритет задачи")
    created_at: datetime = Field(default_factory=datetime.utcnow, title="Дата и время создания задачи")
    owner_id: int = Field(foreign_key="users.id", title="ID владельца задачи")


