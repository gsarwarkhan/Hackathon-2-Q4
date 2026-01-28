# [Task]: T-005
# [From]: specs/constitution.md

from fastapi import FastAPI, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from .routes import tasks
from .db import init_db
from .agent import run_agent
from typing import Dict

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

@app.post("/api/chat")
async def chat_endpoint(payload: Dict = Body(...)):
    user_id = payload.get("user_id", "guest-user")
    message = payload.get("message")
    history = payload.get("history", [])
    
    if not message:
        return {"error": "Message is required"}
    
    response = run_agent(user_id, message, history)
    return {"response": response}

app.include_router(tasks.router)
