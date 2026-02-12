import httpx
import time

BASE_URL = "http://localhost:8001/api"

def test_auth_flow():
    email = f"test_{int(time.time())}@example.com"
    password = "password123"
    
    print("\n--- Testing Registration ---")
    with httpx.Client() as client:
        reg_res = client.post(f"{BASE_URL}/auth/register", json={
            "email": email,
            "password": password,
            "name": "Test User"
        })
        print(f"Registration Status: {reg_res.status_code}")
        print(reg_res.json())
        
        if reg_res.status_code != 200:
            return

        print("\n--- Testing Login ---")
        login_res = client.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": password
        })
        print(f"Login Status: {login_res.status_code}")
        login_data = login_res.json()
        token = login_data.get("access_token")
        print(f"Token Received: {'Yes' if token else 'No'}")
        
        if not token:
            return

        headers = {"Authorization": f"Bearer {token}"}
        
        print("\n--- Testing Authenticated Task List ---")
        task_res = client.get(f"{BASE_URL}/tasks/", headers=headers)
        print(f"Task List Status: {task_res.status_code}")
        print(f"Tasks: {len(task_res.json())}")

        print("\n--- Testing Admin Access (Should fail for normal user) ---")
        admin_res = client.get(f"{BASE_URL}/admin/users", headers=headers)
        print(f"Admin Access (User) Status: {admin_res.status_code} (Expected 403)")

if __name__ == "__main__":
    # Note: Requires the backend server to be running
    print("Ensure the backend server is running at http://localhost:8000")
    try:
        test_auth_flow()
    except Exception as e:
        print(f"Test failed: {e}")
