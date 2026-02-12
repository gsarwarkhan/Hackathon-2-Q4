from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from ..db import get_session
from ..models import User, Task
from ..auth import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List

router = APIRouter(prefix="/api/admin", tags=["admin"])
security = HTTPBearer()

def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = decode_access_token(credentials.credentials)
    if not payload or payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized. Admin role required.")
    return payload

@router.get("/users")
def list_users(session: Session = Depends(get_session), admin=Depends(get_current_admin)):
    """Summary of users for the admin dashboard."""
    users = session.exec(select(User)).all()
    
    summary = []
    for user in users:
        # Count tasks for each user
        task_count = session.exec(select(func.count(Task.id)).where(Task.user_id == user.id)).one()
        summary.append({
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "task_count": task_count,
            "created_at": user.created_at
        })
    return summary
