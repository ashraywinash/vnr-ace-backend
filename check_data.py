"""
Check what data is in the Excel file
"""
import pandas as pd
from pathlib import Path

file_path = Path('data/student_data.xlsx')

df = pd.read_excel(file_path)

print(f"Total records: {len(df)}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nFirst 5 records:")
print(df.head())
print(f"\nBranch distribution:")
print(df['branch'].value_counts())
print(f"\nSample names:")
print(df['name'].head(10).tolist())
