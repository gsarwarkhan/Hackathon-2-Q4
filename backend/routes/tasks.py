# [Task]: T-004
# [From]: specs/features/task-crud.md

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from ..models import Task, User
from ..db import get_session

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# Helper to verify auth (Simplified for now - requires JWT integration logic)
def get_current_user_id():
    # This should come from JWT token verification middleware
    # For initial setup, we might need a dummy or placeholder
    return "guest-user"

@router.get("/", response_model=List[Task])
def read_tasks(
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id),
    status: Optional[str] = None
):
    query = select(Task).where(Task.user_id == user_id)
    if status == "completed":
        query = query.where(Task.is_completed == True)
    elif status == "pending":
        query = query.where(Task.is_completed == False)
    
    return session.exec(query).all()

@router.post("/", response_model=Task)
def create_task(
    task_data: Task,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    task_data.user_id = user_id
    session.add(task_data)
    session.commit()
    session.refresh(task_data)
    return task_data

@router.patch("/{task_id}", response_model=Task)
def update_task(
    task_id: UUID,
    task_update: dict,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in task_update.items():
        setattr(db_task, key, value)
    
    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
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
    return {"ok": True}
