"""
Test script for LLM-based intent classification in classwork graph
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ace_graphs.classwork_graph import classwork_graph

async def test_classwork_graph():
    """Test the classwork graph with various queries"""
    
    test_queries = [
        "Show me CSE students with attendance below 75%",
        "What is the average CGPA of ECE students?",
        "Students with backlogs in year 2",
        "Top performers in CSE section A",
        "CSE students 2nd year with low attendance and poor grades"
    ]
    
    print("=" * 80)
    print("TESTING CLASSWORK GRAPH WITH LLM-BASED INTENT CLASSIFICATION")
    print("=" * 80)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n\n{'='*80}")
        print(f"TEST {i}: {query}")
        print('='*80)
        
        inputs = {
            "user_query": query,
            "role": "admin",
            "context": {}
        }
        
        try:
            result = await classwork_graph.ainvoke(inputs)
            
            print("\n[SUCCESS]")
            print(f"\nFinal Response:")
            print(result.get("final_response", "No response"))
            
        except Exception as e:
            print(f"\n[ERROR]: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_classwork_graph())
