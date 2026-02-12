# [Task]: T-015
# [From]: specs/api/mcp-tools.md

import uuid
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from datetime import datetime, timezone
from sqlmodel import Session, select
from .models import Task
from .db import engine

mcp = FastMCP("todo-mcp")

@mcp.tool()
def add_todo(user_id: str, title: str, description: Optional[str] = None, priority: int = 2) -> str:
    """Create a new task in the user's todo list.
    
    Args:
        user_id: The unique identifier of the user.
        title: The title or summary of the task.
        description: Detailed notes about the task.
        priority: Task priority level (1: Low, 2: Medium, 3: High). Default is 2.
    """
    with Session(engine) as session:
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            priority=priority
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return f"Successfully added task: {task.title} (ID: {task.id})"

@mcp.tool()
def list_todos(user_id: str, status: str = "all") -> str:
    """Retrieve tasks for a user with an optional status filter.
    
    Args:
        user_id: The unique identifier of the user.
        status: Filter tasks by 'all', 'pending', or 'completed'.
    """
    with Session(engine) as session:
        query = select(Task).where(Task.user_id == user_id)
        if status == "completed":
            query = query.where(Task.is_completed == True)
        elif status == "pending":
            query = query.where(Task.is_completed == False)
        
        tasks = session.exec(query).all()
        if not tasks:
            return "No tasks found."
        
        results = []
        for t in tasks:
            status_str = "✅" if t.is_completed else "⭕"
            results.append(f"{status_str} {t.title} [ID: {t.id}]")
        return "\n".join(results)

@mcp.tool()
def complete_todo(user_id: str, todo_id: str) -> str:
    """Mark a task as completed."""
    try:
        t_id = uuid.UUID(todo_id)
    except ValueError:
        return "Invalid Task ID format."

    with Session(engine) as session:
        task = session.get(Task, t_id)
        if not task or task.user_id != user_id:
            return "Task not found."
        
        task.is_completed = True
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        return f"Marked task '{task.title}' as complete."

@mcp.tool()
def delete_todo(user_id: str, todo_id: str) -> str:
    """Delete a task permanently."""
    try:
        t_id = uuid.UUID(todo_id)
    except ValueError:
        return "Invalid Task ID format."

    with Session(engine) as session:
        task = session.get(Task, t_id)
        if not task or task.user_id != user_id:
            return "Task not found."
        
        session.delete(task)
        session.commit()
        return f"Deleted task '{task.title}'."
