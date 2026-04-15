from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User, UserRole
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, payload: TaskCreate, current_user: User) -> Task:
    task = Task(title=payload.title, description=payload.description, owner_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(db: Session, current_user: User) -> list[Task]:
    query = db.query(Task)
    if current_user.role != UserRole.admin:
        query = query.filter(Task.owner_id == current_user.id)
    return query.order_by(Task.id.desc()).all()


def get_task_or_404(db: Session, task_id: int) -> Task:
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


def authorize_task_access(task: Task, current_user: User) -> None:
    if current_user.role == UserRole.admin:
        return
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed for this task")


def update_task(db: Session, task: Task, payload: TaskUpdate) -> Task:
    if payload.title is not None:
        task.title = payload.title
    if payload.description is not None:
        task.description = payload.description
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
