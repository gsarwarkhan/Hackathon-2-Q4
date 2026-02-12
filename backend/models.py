# [Task]: T-002
# [From]: specs/database/schema.md

from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime, timezone
import uuid

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None
    hashed_password: str = Field()
    role: str = Field(default="user")  # "user" or "admin"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    tasks: List["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    priority: int = Field(default=2)  # 1: Low, 2: Medium, 3: High
    is_completed: bool = Field(default=False)
    tags: Optional[str] = None  # Comma separated tags
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: Optional[User] = Relationship(back_populates="tasks")

# --- Pydantic Schemas (DTOs) ---
class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    tags: Optional[str] = None
    priority: int = 2

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    tags: Optional[str] = None
    priority: Optional[int] = None

