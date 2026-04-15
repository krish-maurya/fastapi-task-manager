from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db, require_role
from app.models.user import User, UserRole
from app.schemas.common import MessageResponse
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services.task_service import (
    authorize_task_access,
    create_task,
    delete_task,
    get_task_or_404,
    get_tasks,
    update_task,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskOut:
    return create_task(db, payload, current_user)


@router.get("", response_model=list[TaskOut])
def list_tasks_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TaskOut]:
    return get_tasks(db, current_user)


@router.get("/{task_id}", response_model=TaskOut)
def get_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskOut:
    task = get_task_or_404(db, task_id)
    authorize_task_access(task, current_user)
    return task


@router.put("/{task_id}", response_model=TaskOut)
def update_task_endpoint(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskOut:
    task = get_task_or_404(db, task_id)
    authorize_task_access(task, current_user)
    return update_task(db, task, payload)


@router.delete("/{task_id}", response_model=MessageResponse)
def delete_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.admin)),
) -> MessageResponse:
    task = get_task_or_404(db, task_id)
    delete_task(db, task)
    return MessageResponse(message="Task deleted successfully")
