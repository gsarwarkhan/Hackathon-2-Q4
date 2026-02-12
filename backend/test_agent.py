from .agent import run_agent
import os

def test_agent_interaction():
    user_id = "test-user-001"
    
    print("\n--- Testing Agent: Add Task ---")
    response1 = run_agent(user_id, "Add a high priority task to 'Review security protocols' with the description 'Check all environment variables are secure.'")
    print(f"Agent Response: {response1}")
    
    print("\n--- Testing Agent: List Tasks ---")
    response2 = run_agent(user_id, "What are my current tasks?")
    print(f"Agent Response: {response2}")
    
    print("\n--- Testing Agent: Complete Task ---")
    # This might require parsing the ID from the previous response if we wanted to be robust,
    # but for a manual verification we'll look at the output.
    response3 = run_agent(user_id, "Mark the security review task as complete.")
    print(f"Agent Response: {response3}")

if __name__ == "__main__":
    # Check if API Key is available
    if not os.getenv("GOOGLE_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        print("ERROR: No API Key found in environment variables.")
    else:
        try:
            test_agent_interaction()
        except Exception as e:
            print(f"Verification Failed: {e}")
