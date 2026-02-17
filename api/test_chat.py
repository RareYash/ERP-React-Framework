"""
Test script for the Chatbot API endpoints.
Verifies structure and function calling logic.
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE = "http://localhost:8000"
API_KEY = os.getenv("GEMINI_API_KEY")

def test_chat():
    print("=== Testing Chat Endpoint ===")
    
    # 1. Login to get token
    print("Logging in...")
    try:
        r = requests.post(f"{BASE}/api/auth/login", json={"username": "teacher", "password": "admin1234"})
        if r.status_code != 200:
            print(f"Login failed: {r.status_code} {r.text}")
            return
        
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("Login successful.")

        # 2. Send chat message
        print("\nSending chat message: 'How is Aarav doing?'")
        # If API key is missing/invalid, backend will return 500 or error message in reply
        
        payload = {
            "message": "How is Aarav doing?",
            "history": []
        }
        
        r = requests.post(f"{BASE}/api/chat", json=payload, headers=headers)
        
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"Reply: {data.get('reply')[:100]}...")
            print(f"Action Taken: {data.get('action_taken')}")
            
            # Additional check: structure
            if "reply" in data:
                print("PASS: valid response structure")
            else:
                print("FAIL: missing reply field")
                
        else:
            print(f"Error response: {r.text}")
            if "Gemini API key not configured" in r.text or "API key not valid" in r.text:
                 print("(Expected if API key is missing/invalid)")

    except Exception as e:
        print(f"Test failed with exception: {e}")

if __name__ == "__main__":
    if not API_KEY or API_KEY == "your_api_key_here":
        print("WARNING: GEMINI_API_KEY is not set in .env or is placeholder.")
        print("Tests will likely fail or return configuration error.")
    
    test_chat()
