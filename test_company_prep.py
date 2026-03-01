"""
Test the company prep Q&A feature
"""
import requests
import json

url = "http://localhost:8000/placements/prep/company-questions"
headers = {"Content-Type": "application/json"}

# Test with Google
print("="*80)
print("Testing Company Prep Q&A Feature")
print("="*80)

test_cases = [
    {"company_name": "Google", "job_role": "Software Engineer"},
    {"company_name": "Amazon", "job_role": "SDE"},
    {"company_name": "Microsoft", "job_role": "Software Developer"},
]

for test in test_cases:
    print(f"\n\nTest: {test['company_name']} - {test['job_role']}")
    print("-"*80)
    
    try:
        response = requests.post(url, headers=headers, json=test)
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✓ Success!")
            print(f"  Company: {result.get('company')}")
            print(f"  Role: {result.get('role')}")
            print(f"  Questions generated: {len(result.get('questions', []))}")
            print(f"  Context loaded: {result.get('context_loaded')}")
            print(f"  Web search results: {result.get('web_search_results')}")
            
            # Show first 3 questions
            questions = result.get('questions', [])
            if questions:
                print(f"\n  Sample Questions:")
                for i, q in enumerate(questions[:3], 1):
                    print(f"    {i}. [{q.get('category')}] {q.get('question')}")
                    print(f"       Difficulty: {q.get('difficulty')}")
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"  {response.text}")
            
    except Exception as e:
        print(f"✗ Exception: {e}")

print("\n" + "="*80)
print("Test Complete!")
print("="*80)
