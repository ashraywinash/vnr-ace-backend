import requests

url = "http://localhost:8000/placements/prep/previous-questions"
params = {"company_name": "Google"}

print(f"Testing GET {url} with params {params}")
response = requests.get(url, params=params)

print(f"Status Code: {response.status_code}")
try:
    print("Response JSON:")
    print(response.json())
except Exception as e:
    print(f"Response text: {response.text}")
