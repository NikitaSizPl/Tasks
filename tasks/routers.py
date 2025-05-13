from database.database import SessionDep
from tasks.models import Tasks
from fastapi import Depends, HTTPException, APIRouter
from .schemas import TaskRead, TaskCreate, TaskUpdate
from auth.utils import get_current_user


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, session: SessionDep, user=Depends(get_current_user)):
    new_task = Tasks(**task.dict(), owner_id=user.id)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@router.put("/{task_id}/")
def update_task(task_id: int, task_data: TaskUpdate, session: SessionDep, user=Depends(get_current_user)):
    task = session.query(Tasks).filter(Tasks.id == task_id, Tasks.owner_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in task_data.dict(exclude_unset=True).items():
        setattr(task, field, value)
    session.commit()
    session.refresh(task)
    return task


@router.get("/", response_model=list[TaskRead])
def get_tasks(session: SessionDep,user=Depends(get_current_user)):
    query = session.query(Tasks).filter(Tasks.owner_id == user.id)
    tasks = query.all()
    return tasks


@router.get("/search", response_model=list[TaskRead])
def search_tasks(search: str,  session: SessionDep, user=Depends(get_current_user)
):
    tasks = session.query(Tasks).filter(
        Tasks.owner_id == user.id,
            Tasks.title.ilike(f"%{search}%"),
            Tasks.description.ilike(f"%{search}%")
        ).all()
    return tasks