# MCP Tools Specification

The MCP server exposes the following tools to allow the AI Agent to manage tasks.

## Tools

### `add_todo`
- **Purpose**: Creates a new task.
- **Arguments**:
    - `title` (string, required)
    - `description` (string, optional)
    - `priority` (integer, optional: 1-3)
    - `tags` (string, optional: comma-separated)

### `list_todos`
- **Purpose**: Retrieves tasks based on filters.
- **Arguments**:
    - `status` (string, optional: "all", "pending", "completed")

### `complete_todo`
- **Purpose**: Marks a task as completed.
- **Arguments**:
    - `todo_id` (uuid, required)

### `delete_todo`
- **Purpose**: Deletes a task permanently.
- **Arguments**:
    - `todo_id` (uuid, required)

### `update_todo`
- **Purpose**: Updates task details.
- **Arguments**:
    - `todo_id` (uuid, required)
    - `title` (string, optional)
    - `description` (string, optional)
    - `priority` (integer, optional)
