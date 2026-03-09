import asyncio
import pandas as pd
import sys
import os
import math

# Add root project path to Python path so we can import core/models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.db import AsyncSessionLocal
from models.student import Student
from sqlalchemy import select

async def main():
    file_path = "data/placed_unplaced.xlsx"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
        
    print(f"Reading {file_path}...")
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Failed to read excel: {e}")
        return
        
    async with AsyncSessionLocal() as session:
        for index, row in df.iterrows():
            if pd.isna(row.get('Roll No')):
                continue
                
            roll_no = str(row['Roll No']).strip()
            
            # Check if exists
            stmt = select(Student).where(Student.roll_no == roll_no)
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if existing:
                print(f"Skipping {roll_no}, already exists.")
                continue
                
            # Helper to safely clean NaNs from pandas
            def safe_get(val, default):
                return default if pd.isna(val) else val
            
            # Map Excel columns to DB model fields (matching structure vaguely typical for this domain)
            student = Student(
                roll_no=roll_no,
                full_name=safe_get(row.get('Student Name'), None),
                gender=safe_get(row.get('Gender'), None),
                branch=safe_get(row.get('Branch'), None),
                email=safe_get(row.get('Email'), None),
                mobile=str(safe_get(row.get('Mobile'), "")) if not pd.isna(row.get('Mobile')) else None,
                cgpa=float(safe_get(row.get('CGPA'), 0.0)),
                tenth_cgpa=float(safe_get(row.get('10th % / CGPA'), 0.0)),
                inter_percent=float(safe_get(row.get('Inter %'), 0.0)),
                active_backlogs=int(safe_get(row.get('Active Backlogs'), 0)),
                passive_backlogs=int(safe_get(row.get('History of Backlogs'), 0)),
                category=safe_get(row.get('Category'), None),
                home_town=safe_get(row.get('Home Town'), None),
                district=safe_get(row.get('District'), None),
                state=safe_get(row.get('State'), None),
                pincode=str(safe_get(row.get('Pincode'), "")),
            )
            
            session.add(student)
        
        print("Committing to database...")
        await session.commit()
    print("Student import complete.")

if __name__ == "__main__":
    asyncio.run(main())
