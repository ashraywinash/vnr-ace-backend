"""
Simple test for classwork module
"""
import asyncio
from ace_graphs.classwork_graph import classwork_graph

async def main():
    print("Testing: CSE students in 2nd year")
    
    inputs = {
        "user_query": "Show me CSE students in 2nd year",
        "role": "admin",
        "context": {}
    }
    
    result = await classwork_graph.ainvoke(inputs)
    
    print("\n" + result["final_response"])

if __name__ == "__main__":
    asyncio.run(main())
