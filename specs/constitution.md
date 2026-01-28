# Project Constitution

## Core Principles
1. **Spec-Driven**: No code is written without a validated task and spec.
2. **Clean Architecture**: Separation of concerns between UI, API, and Persistence.
3. **Type Safety**: Use TypeScript for frontend and Pydantic/SQLModel for backend.
4. **User-Centric**: Professional, premium UI with a focus on usability.

## Tech Stack (Phase II+)
- **Frontend**: Next.js 16 (App Router), Tailwind CSS.
- **Backend**: FastAPI, Python 3.13+.
- **ORM/DB**: SQLModel, Neon Serverless PostgreSQL.
- **Auth**: Better Auth with JWT integration for FastAPI.
- **AI**: OpenAI Agents SDK, MCP (Phase III+).

## Coding Standards
- **Naming**: Descriptive, snake_case for Python, camelCase for JS.
- **Structure**: Monorepo with `/frontend` and `/backend` directories.
- **Documentation**: All public endpoints and complex logic must be documented in specs.
