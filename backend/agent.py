import os
import google.generativeai as genai
from .mcp_server import add_todo, list_todos, complete_todo, delete_todo

# Capture and then clear environment variables to avoid SDK confusion
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")

if not api_key or "your" in api_key.lower():
    raise ValueError("Valid Gemini API Key not found. Please set GOOGLE_API_KEY system variable.")

# Clean the key
api_key = api_key.strip().strip('"').strip("'")
genai.configure(api_key=api_key)

SYSTEM_PROMPT = """
You are the Evolution of Todo AI Assistant. Your goal is to help users manage their tasks efficiently.
You have access to tools to interact with the user's todo list.
When a user asks to do something (add, list, complete, delete), use the appropriate tool.
Always pass the provided 'user_id' to the tools.
If a user mentions a task but doesn't provide a title, ask for clarification.
Confirm the action you've taken clearly and professionally.
"""

def run_agent(user_id: str, user_message: str, history: list = []):
    # Bind tools to the model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT,
        tools=[add_todo, list_todos, complete_todo, delete_todo]
    )
    
    # Send message with automatic tool calling
    chat = model.start_chat(history=history, enable_automatic_function_calling=True)
    response = chat.send_message(f"[User: {user_id}] {user_message}")
    
    return response.text
