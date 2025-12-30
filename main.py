"""
Evolution of Todo - Final Polish (The Engine)
Core business logic and persistence layer with enhanced robustness and documentation.
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
    """Domain Value Object: Task priority levels.

    Attributes:
        LOW (1): Least urgent.
        MEDIUM (2): Standard urgency.
        HIGH (3): Most urgent.
    """
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass(frozen=True, slots=True)
class Task:
    """Domain Entity representing a ToDo task.

    Attributes:
        id (uuid.UUID): Unique identifier for the task.
        title (str): The main summary of the task.
        description (str): Detailed notes about the task.
        is_completed (bool): Status of task completion.
        tags (List[str]): Organizational categories.
        priority (Priority): Importance level.
        created_at (datetime): Timestamp of creation (UTC).
    """
    id: uuid.UUID
    title: str
    description: str = ""
    is_completed: bool = False
    tags: List[str] = field(default_factory=list)
    priority: Priority = Priority.MEDIUM
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def toggle(self) -> "Task":
        """Returns a new Task instance with toggled completion status.

        Returns:
            Task: A new immutable Task instance with inverted is_completed state.
        """
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
        """Returns a new Task instance with updated fields.

        Args:
            title: New title string.
            description: New description string.
            tags: New list of tags.
            priority: New Priority level.

        Returns:
            Task: A new immutable Task instance with modified fields.
        """
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
    """Infrastructure Layer: Handles JSON persistence with full hydration and error resilience."""

    def __init__(self, file_path: str = "tasks.json") -> None:
        """Initializes the storage with a specific file path.

        Args:
            file_path: Relative or absolute path to the JSON storage file.
        """
        self.file_path = Path(file_path)

    def save(self, tasks: List[Task]) -> None:
        """Serializes and saves tasks to a JSON file.

        Args:
            tasks: List of Task entities to persist.
        """
        try:
            data = []
            for task in tasks:
                task_dict = asdict(task)
                task_dict["id"] = str(task_dict["id"])
                task_dict["priority"] = task.priority.name
                task_dict["created_at"] = task_dict["created_at"].isoformat()
                data.append(task_dict)

            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"CRITICAL: Failed to save to {self.file_path}: {e}")

    def load(self) -> List[Task]:
        """Loads and hydrates tasks from JSON with corruption resilience.

        Returns:
            List[Task]: Hydrated Task instances. Returns empty list if file missing or corrupt.
        """
        if not self.file_path.exists():
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)

            tasks = []
            for item in data:
                try:
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
                except (KeyError, ValueError, TypeError) as e:
                    print(f"WARNING: Skipping corrupted task entry: {e}")
                    continue
            return tasks
        except (json.JSONDecodeError, IOError) as e:
            print(f"ERROR: Could not load data from {self.file_path} ({e}). Recovering with empty list.")
            return []


class TodoManager:
    """Business Logic Layer: Orchestrates task mutations and domain rules."""

    def __init__(self, storage: StorageManager) -> None:
        """Initializes manager and performs initial hydration.

        Args:
            storage: A StorageManager instance for state persistence.
        """
        self.storage = storage
        self._tasks: List[Task] = self.storage.load()

    def _persist(self) -> None:
        """Triggers the persistence layer to save current state."""
        self.storage.save(self._tasks)

    def add_task(self, title: str, description: str = "", tags: List[str] = [], priority: Priority = Priority.MEDIUM) -> Task:
        """Requirement UC-1: Add a validated task to the system.

        Args:
            title: Summary of task.
            description: Optional details.
            tags: Categorization strings.
            priority: Importance level.

        Returns:
            Task: The newly created task.

        Raises:
            ValueError: If title is empty or whitespace.
        """
        if not title.strip():
            raise ValueError("Task title is required and cannot be blank.")

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
        """Requirement UC-2 & UC-8: Retrieve sorted and filtered tasks.

        Args:
            tag_filter: Optional tag name to filter results (case-insensitive).

        Returns:
            List[Task]: Sorted list (Priority DSC > Date DSC).
        """
        tasks = self._tasks
        if tag_filter:
            target = tag_filter.lower().strip()
            tasks = [t for t in tasks if any(target == tag.lower() for tag in t.tags)]

        # Sorted by Priority (HIGH -> LOW) then Created At (Newest first)
        return sorted(tasks, key=lambda t: (t.priority.value, t.created_at.timestamp()), reverse=True)

    def update_task(self, task_id: uuid.UUID, **kwargs) -> Task:
        """Requirement UC-3: Modify an existing task.

        Args:
            task_id: UUID of target task.
            **kwargs: Fields to update (title, description, tags, priority).

        Returns:
            Task: The updated task instance.
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                updated = task.update(**kwargs)
                self._tasks[i] = updated
                self._persist()
                return updated
        raise KeyError(f"Task with ID {task_id} not found.")

    def delete_task(self, task_id: uuid.UUID) -> None:
        """Requirement UC-4: Permanently remove a task."""
        self._tasks = [t for t in self._tasks if t.id != task_id]
        self._persist()

    def toggle_task(self, task_id: uuid.UUID) -> Task:
        """Requirement UC-5: Toggle the completion status."""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                updated = task.toggle()
                self._tasks[i] = updated
                self._persist()
                return updated
        raise KeyError(f"Task with ID {task_id} not found.")

    def clear_completed(self) -> int:
        """Requirement: Housekeeping - remove all tasks marked as completed.

        Returns:
            int: Number of tasks cleared.
        """
        original_count = len(self._tasks)
        self._tasks = [t for t in self._tasks if not t.is_completed]
        cleared_count = original_count - len(self._tasks)
        if cleared_count > 0:
            self._persist()
        return cleared_count


if __name__ == "__main__":
    print("Evolution of Todo: Engine Ready.")
