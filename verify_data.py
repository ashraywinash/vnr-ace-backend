"""
Test the actual data being loaded by the graph
"""
import asyncio
import pandas as pd
from pathlib import Path

async def main():
    # Check what's in the Excel file
    file_path = Path('data/student_data.xlsx')
    df = pd.read_excel(file_path)
    
    print("="*80)
    print("EXCEL FILE CONTENTS")
    print("="*80)
    print(f"Total records: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nFirst 10 student names:")
    for i, name in enumerate(df['name'].head(10), 1):
        print(f"  {i}. {name}")
    
    print(f"\nBranch distribution: {df['branch'].value_counts().to_dict()}")
    
    # Now test what the graph reads
    print("\n" + "="*80)
    print("GRAPH DATA LOADING TEST")
    print("="*80)
    
    from ace_graphs.classwork_graph import classwork_graph
    
    inputs = {
        "user_query": "Show all students",
        "role": "admin",
        "context": {}
    }
    
    result = await classwork_graph.ainvoke(inputs)
    dataset = result.get('unified_dataset', [])
    
    print(f"Records loaded by graph: {len(dataset)}")
    if dataset:
        print(f"\nFirst 5 students from graph:")
        for i, student in enumerate(dataset[:5], 1):
            print(f"  {i}. {student['name']} - {student['roll_number']} - {student['branch']}")

if __name__ == "__main__":
    asyncio.run(main())
