# Database Schema: SQLModel

## Tables

### `User` (Managed by Better Auth)
- `id`: string (PK)
- `email`: string (Unique)
- `name`: string
- `created_at`: datetime

### `Task` (Managed by FastAPI)
- `id`: uuid (PK)
- `user_id`: string (FK -> User.id)
- `title`: string (Required)
- `description`: text (Optional)
- `priority`: integer (Default: 2 - Medium)
- `is_completed`: boolean (Default: False)
- `tags`: JSON/Array of strings
- `created_at`: datetime (ISO 8601)
- `updated_at`: datetime

## Relationships
- User (1) <---> (N) Task
