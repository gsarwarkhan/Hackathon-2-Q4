# [Task]: T-016
# [From]: specs/features/chatbot.md

import os
import google.generativeai as genai
from .mcp_server import mcp

# Configure Gemini
genai.configure(api_key=os.getenv("OPENAI_API_KEY")) # Using the slot where user pasted the key

SYSTEM_PROMPT = """
You are the evolution of Todo AI Assistant. Your goal is to help users manage their tasks efficiently.
You have access to a set of tools to interact with the user's todo list.
Always be professional, concise, and helpful. 
When a user asks to do something, use the appropriate tool.
If a user mentions a task but doesn't provide a title, ask for clarification.
Confirm the action you've taken clearly.
"""

def run_agent(user_id: str, user_message: str, history: list = []):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )
    
    chat = model.start_chat(history=history)
    
    # 1. Generate Content
    response = chat.send_message(user_message)
    
    # 2. Handle Tool Calls (Conceptual for this phase)
    # Note: Gemini has built-in function calling. 
    # For the Hackathon demonstration, we ensure the agent is connected.
    
    return response.text
