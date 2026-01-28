# [Task]: T-002
# [From]: specs/database/schema.md

from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    tasks: List["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    priority: int = Field(default=2)  # 1: Low, 2: Medium, 3: High
    is_completed: bool = Field(default=False)
    tags: Optional[str] = None  # Comma separated tags
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="tasks")
