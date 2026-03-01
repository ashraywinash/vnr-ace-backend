"""
Direct API test to show exactly what the backend returns
"""
import requests
import json

url = "http://localhost:8000/classwork/chat"
headers = {"Content-Type": "application/json"}

# Test with the same query
data = {"message": "Show me all students"}

try:
    print("Testing API endpoint...")
    print(f"URL: {url}")
    print(f"Query: {data['message']}\n")
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        reply = result.get('reply', '')
        
        print("="*80)
        print("BACKEND RESPONSE")
        print("="*80)
        print(reply)
        print("\n" + "="*80)
        
        # Check which data is being returned
        if 'Aarav Sharma' in reply and '21R01A0501' in reply:
            print("\n✅ BACKEND IS CORRECT: Returning NEW student data")
            print("   Students: Aarav Sharma, Vivaan Patel, Aditya Kumar, etc.")
            print("   Roll numbers: 21R01A0501-21R01A0530")
        elif 'Bhavna' in reply or 'Ishaan' in reply:
            print("\n❌ BACKEND HAS OLD DATA: Still returning old students")
            print("   This means the Excel file wasn't updated properly")
        
        print("\n" + "="*80)
        print(f"Metadata: {result.get('metadata', {})}")
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error connecting to API: {e}")
