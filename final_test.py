"""
Final verification - show exactly what the API returns
"""
import requests

url = "http://localhost:8000/classwork/chat"

# Test query
response = requests.post(url, json={"message": "Show all students"})

if response.status_code == 200:
    result = response.json()
    reply = result['reply']
    
    # Extract first few student names from the response
    lines = reply.split('\n')
    student_lines = [l for l in lines if '|' in l and 'Name' not in l and '---' not in l][:5]
    
    print("="*80)
    print("ACTUAL API RESPONSE - First 5 Students")
    print("="*80)
    for line in student_lines:
        print(line)
    
    print("\n" + "="*80)
    
    # Check which dataset
    if 'Aarav Sharma' in reply:
        print("✅ API IS RETURNING NEW DATA")
        print("   First student: Aarav Sharma (21R01A0501)")
    elif 'Bhavna' in reply:
        print("❌ API IS RETURNING OLD DATA") 
        print("   First student: Bhavna")
    
    print(f"\nTotal records: {result.get('metadata', {}).get('record_count', 'unknown')}")
else:
    print(f"Error: {response.status_code}")
