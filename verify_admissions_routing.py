import asyncio
import os
from ace_graphs.admissions_graph import admissions_graph, DEPARTMENTS_DATA

async def test_department(query, expected_dept=None):
    print(f"\nTesting Query: {query}")
    initial_state = {
        "message": query,
        "reply": None,
        "route": None,
        "dept_route": None
    }
    
    result = await admissions_graph.ainvoke(initial_state)
    print(f"Route: {result.get('route')}")
    print(f"Dept Route: {result.get('dept_route')}")
    print(f"Reply: {result.get('reply')}")
    
    if expected_dept:
        if result.get('dept_route') == expected_dept:
            print(f"[OK] CORRECT: Routed to {expected_dept}")
        else:
            print(f"[FAIL] ERROR: Expected {expected_dept}, got {result.get('dept_route')}")

async def main():
    print("Listing loaded departments:")
    for key in DEPARTMENTS_DATA.keys():
        print(f"- {key}")

    # Test case 1: General Admissions
    await test_department("Tell me about VNR admissions fees", "admissions")
    
    # Test case 2: Specific Department (Biotech)
    await test_department("What is the mission of Biotechnology department?", "department_of_biotechnology")
    
    # Test case 3: Out of scope for a department (should return fallback)
    await test_department("What is the parking fee for Biotechnology students?", "department_of_biotechnology")
    
    # Test case 4: Non-department query that goes to FAQ
    await test_department("Who is the Prime Minister of India?", None)

if __name__ == "__main__":
    asyncio.run(main())
