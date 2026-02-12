# [Task]: T-004
# [From]: specs/features/task-crud.md

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from datetime import datetime, timezone
from ..models import Task, TaskCreate, TaskUpdate
from ..db import get_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..auth import decode_access_token

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

security = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Validates JWT and returns the user ID (sub)."""
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user identity",
        )
    return user_id

@router.get("/", response_model=List[Task])
def read_tasks(
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id),
    status: str | None = None
):
    query = select(Task).where(Task.user_id == user_id)
    if status == "completed":
        query = query.where(Task.is_completed == True)
    elif status == "pending":
        query = query.where(Task.is_completed == False)
    
    return session.exec(query).all()

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    task = Task.model_validate(task_in)
    task.user_id = user_id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.patch("/{task_id}", response_model=Task)
def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    db_task.updated_at = datetime.now(timezone.utc)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(db_task)
    session.commit()
    return None
