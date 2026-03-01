import requests

BASE_URL = "http://localhost:8000"

def test_auth_flow():
    print(">>> Testing Auth Flow & Student Chat <<<")
    
    # 1. Login as Student
    print("\n1. Logging in as Student...")
    login_data = {
        "username": "student@vnr.edu.in",
        "password": "student123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return
        
    token_data = response.json()
    access_token = token_data["access_token"]
    print(f"Login successful! User ID: {token_data['user']['id']}")
    
    # 2. Call Student Chat API
    print("\n2. Calling Student Chat API...")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    chat_payload = {
        "message": "Where is Dr. Ravi Kumar?"
    }
    
    chat_response = requests.post(
        f"{BASE_URL}/classwork/student/chat", 
        json=chat_payload, 
        headers=headers
    )
    
    if chat_response.status_code == 200:
        print("Chat successful!")
        print(f"Reply: {chat_response.json().get('reply')}")
    else:
        print(f"Chat failed: {chat_response.text}")

if __name__ == "__main__":
    try:
        test_auth_flow()
    except Exception as e:
        print(f"Test failed: {e}")
