# Feature: Task CRUD Operations

## User Stories
- As a user, I want to create tasks with a title, description, and priority.
- As a user, I want to categorize tasks with tags.
- As a user, I want to see a list of my tasks, filtered by status or tags.
- As a user, I want to update or delete my tasks.
- As a user, I want to mark tasks as complete/incomplete.

## Acceptance Criteria
- [ ] Tasks must be private to the authenticated user.
- [ ] Title is required; description and tags are optional.
- [ ] Priority must be one of: LOW, MEDIUM, HIGH.
- [ ] Data must persist in the Neon PostgreSQL database.

## Technical Details
- **Backend Model**: `Task` SQLModel.
- **Frontend Views**: Dashboard with task list, and a "Seed New Task" form.
- **Endpoints**:
    - `POST /api/tasks`: Create task.
    - `GET /api/tasks`: List tasks (with filters).
    - `PATCH /api/tasks/{id}`: Update task/toggle status.
    - `DELETE /api/tasks/{id}`: Delete task.
