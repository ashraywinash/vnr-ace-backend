"""
Test script for classwork module
"""
import asyncio
from ace_graphs.classwork_graph import classwork_graph

async def test_query(query: str):
    print(f"\n{'='*80}")
    print(f"QUERY: {query}")
    print(f"{'='*80}")
    
    inputs = {
        "user_query": query,
        "role": "admin",
        "context": {}
    }
    
    result = await classwork_graph.ainvoke(inputs)
    
    print("\nRESPONSE:")
    print(result["final_response"])
    print(f"\nRecords returned: {len(result.get('unified_dataset', []))}")

async def main():
    print("Testing Classwork Module - Excel Integration")
    print("=" * 80)
    
    # Test 1: Basic branch and year filter
    await test_query("Show me CSE students in 2nd year")
    
    # Test 2: Attendance-based query
    await test_query("Students with attendance less than 75%")
    
    # Test 3: CGPA-based query
    await test_query("Top performers with CGPA above 8.5")
    
    # Test 4: Combined filters
    await test_query("CSE students with low attendance and backlogs")
    
    # Test 5: Backlog-specific query
    await test_query("Students with more than 2 backlogs")
    
    # Test 6: Section-based query
    await test_query("Show section A students in ECE branch")
    
    print("\n" + "="*80)
    print("All tests completed!")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())
