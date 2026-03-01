"""
Test API endpoint to verify current data
"""
import requests
import json

url = "http://localhost:8000/classwork/chat"
headers = {"Content-Type": "application/json"}

# Test query
data = {"message": "Show me all CSE students"}

try:
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        print("="*80)
        print("API RESPONSE")
        print("="*80)
        print(f"Status: {response.status_code}")
        print(f"\nMetadata: {result.get('metadata', {})}")
        print(f"\nResponse Preview (first 500 chars):")
        print(result.get('reply', '')[:500])
        print("\n" + "="*80)
        
        # Check for specific student names to verify data
        reply = result.get('reply', '')
        if 'Aarav Sharma' in reply or 'Vivaan Patel' in reply:
            print("✓ CORRECT: New student data is being loaded!")
        elif 'Bhavna' in reply or 'Ishaan' in reply:
            print("✗ ISSUE: Old student data is still being returned!")
        else:
            print("? UNKNOWN: Cannot determine which dataset is being used")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"Error connecting to API: {e}")
    print("\nMake sure the server is running: poetry run uvicorn app:app --reload")
