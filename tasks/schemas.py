from pydantic import BaseModel
from datetime import datetime
from .models import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.pending
    priority: int = 1
    created_at: datetime | None = None


class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: TaskStatus
    priority: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: int | None = None
