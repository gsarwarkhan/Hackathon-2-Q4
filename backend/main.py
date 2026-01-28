# [Task]: T-005
# [From]: specs/constitution.md

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import tasks
from .db import init_db

app = FastAPI(title="Evolution of Todo API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Evolution of Todo API", "docs": "/docs"}

app.include_router(tasks.router)
