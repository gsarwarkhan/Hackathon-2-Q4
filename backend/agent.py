# [Task]: T-016
# [From]: specs/features/chatbot.md

import os
from openai import OpenAI
from .mcp_server import mcp

# This is a conceptual integration of the OpenAI Agents SDK pattern
# In a real production environment, you'd use the Agents SDK's Runner
# For this phase, we'll implement the core logic using standard OpenAI Tools calling 
# which is the foundation of the Agents SDK.

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are the evolution of Todo AI Assistant. Your goal is to help users manage their tasks efficiently.
You have access to a set of MCP tools to interact with the user's todo list.
Always be professional, concise, and helpful. 
When a user asks to do something, use the appropriate tool.
If a user mentions a task but doesn't provide a title, ask for clarification.
Confirm the action you've taken clearly.
"""

def run_agent(user_id: str, user_message: str, history: list = []):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": user_message}
    ]

    # 1. Initial LLM Call
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=mcp.get_tools_for_openai() # Helper assumes mcp server exposes tool metadata
    )

    # 2. Handle Tool Calls
    tool_calls = response.choices[0].message.tool_calls
    if tool_calls:
        messages.append(response.choices[0].message)
        for tool_call in tool_calls:
            # Inject user_id into tool arguments automatically
            import json
            args = json.loads(tool_call.function.arguments)
            args["user_id"] = user_id
            
            # Call the tool function via the MCP server
            result = mcp.call_tool(tool_call.function.name, args)
            
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": tool_call.function.name,
                "content": result
            })
        
        # 3. Final LLM Response after tool execution
        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return final_response.choices[0].message.content
    
    return response.choices[0].message.content
