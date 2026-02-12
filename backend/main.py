# [Task]: T-005
# [From]: specs/constitution.md
# [SYSTEM]: NEURAL PROTOCOL RELOADED

from fastapi import FastAPI, Depends, Body, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .routes import tasks, auth, admin
from .db import init_db
from .agent import run_agent
from typing import Dict

app = FastAPI(title="Evolution of Todo API")

# Configure CORS - Google-Grade Open Access for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, # Must be false if origins is *
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/api/health")
def health():
    return {"status": "ok", "engine": "aurora-v3"}

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

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(tasks.router)
