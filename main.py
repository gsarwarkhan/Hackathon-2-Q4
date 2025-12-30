"""
Evolution of Todo - Phase VI (The Engine)
Core business logic and persistence layer.
Built by Khizr for Ghulam Sarwar Khan for GIAIC Hackathon II.
"""

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import IntEnum
from pathlib import Path
from typing import List, Optional


class Priority(IntEnum):
    """Domain Value Object: Task priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass(frozen=True, slots=True)
class Task:
    """Domain Entity representing a ToDo task."""
    id: uuid.UUID
    title: str
    description: str = ""
    is_completed: bool = False
    tags: List[str] = field(default_factory=list)
    priority: Priority = Priority.MEDIUM
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def toggle(self) -> "Task":
        """Returns a new Task instance with toggled completion status."""
        return Task(
            id=self.id,
            title=self.title,
            description=self.description,
            is_completed=not self.is_completed,
            tags=self.tags,
            priority=self.priority,
            created_at=self.created_at
        )

    def update(self,
               title: Optional[str] = None,
               description: Optional[str] = None,
               tags: Optional[List[str]] = None,
               priority: Optional[Priority] = None) -> "Task":
        """Returns a new Task instance with updated fields."""
        return Task(
            id=self.id,
            title=title if title is not None else self.title,
            description=description if description is not None else self.description,
            is_completed=self.is_completed,
            tags=tags if tags is not None else self.tags,
            priority=priority if priority is not None else self.priority,
            created_at=self.created_at
        )


class StorageManager:
    """Infrastructure Layer: Handles JSON persistence with full hydration."""

    def __init__(self, file_path: str = "tasks.json") -> None:
        self.file_path = Path(file_path)

    def save(self, tasks: List[Task]) -> None:
        """Serializes and saves tasks to a JSON file."""
        data = []
        for task in tasks:
            task_dict = asdict(task)
            task_dict["id"] = str(task_dict["id"])
            task_dict["priority"] = task.priority.name
            task_dict["created_at"] = task_dict["created_at"].isoformat()
            data.append(task_dict)

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load(self) -> List[Task]:
        """Loads and hydrates tasks from JSON."""
        if not self.file_path.exists():
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            tasks = []
            for item in data:
                tasks.append(
                    Task(
                        id=uuid.UUID(item["id"]),
                        title=item["title"],
                        description=item["description"],
                        is_completed=item["is_completed"],
                        tags=item.get("tags", []),
                        priority=Priority[item.get("priority", "MEDIUM")],
                        created_at=datetime.fromisoformat(item["created_at"])
                    )
                )
            return tasks
        except (json.JSONDecodeError, KeyError, ValueError):
            return []


class TodoManager:
    """Business Logic Layer: Orchestrates task mutations."""

    def __init__(self, storage: StorageManager) -> None:
        self.storage = storage
        self._tasks: List[Task] = self.storage.load()

    def _persist(self) -> None:
        self.storage.save(self._tasks)

    def add_task(self, title: str, description: str = "", tags: List[str] = [], priority: Priority = Priority.MEDIUM) -> Task:
        """Requirement: Add Task"""
        if not title.strip():
            raise ValueError("Title is required.")

        new_task = Task(
            id=uuid.uuid4(),
            title=title.strip(),
            description=description.strip(),
            tags=[tag.strip() for tag in tags if tag.strip()],
            priority=priority
        )
        self._tasks.append(new_task)
        self._persist()
        return new_task

    def get_all_tasks(self, tag_filter: Optional[str] = None) -> List[Task]:
        """Requirement: Composite Sort & Search"""
        tasks = self._tasks
        if tag_filter:
            target = tag_filter.lower().strip()
            tasks = [t for t in tasks if any(target == tag.lower() for tag in t.tags)]

        # Sorted by Priority (HIGH -> LOW) then Created At (Newest first)
        return sorted(tasks, key=lambda t: (t.priority.value, t.created_at.timestamp()), reverse=True)

    def update_task(self, task_id: uuid.UUID, **kwargs) -> Task:
        """Requirement: Update Task"""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                updated = task.update(**kwargs)
                self._tasks[i] = updated
                self._persist()
                return updated
        raise KeyError(f"Task {task_id} not found.")

    def delete_task(self, task_id: uuid.UUID) -> None:
        """Requirement: Delete Task"""
        self._tasks = [t for t in self._tasks if t.id != task_id]
        self._persist()

    def toggle_task(self, task_id: uuid.UUID) -> Task:
        """Requirement: Toggle Task"""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                updated = task.toggle()
                self._tasks[i] = updated
                self._persist()
                return updated
        raise KeyError(f"Task {task_id} not found.")


if __name__ == "__main__":
    # Library mode. Demo available via app.py.
    print("Evolution of Todo: Core Engine Loaded.")
