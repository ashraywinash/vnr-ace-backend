import asyncio
import pandas as pd
import sys
import os
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.db import AsyncSessionLocal
from models.student import Student
from models.company import Company
from models.placement import Placement
from sqlalchemy import select

async def get_student_id(session, roll_no):
    stmt = select(Student.id).where(Student.roll_no == roll_no)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
    
async def get_company_id(session, name):
    stmt = select(Company.id).where(Company.name == name)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def main():
    file_path = "data/consolidated.xlsx"
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
            roll_val = row.get('Roll No')
            comp_val = row.get('Company Name')
            
            if pd.isna(roll_val) or pd.isna(comp_val):
                continue
                
            roll_no = str(roll_val).strip()
            comp_name = str(comp_val).strip()
            
            student_id = await get_student_id(session, roll_no)
            company_id = await get_company_id(session, comp_name)
            
            if not student_id or not company_id:
                print(f"Skipping row {index}: Mismatched student or company IDs")
                continue
            
            ctc = row.get('CTC (LPA)')
            ctc_value = float(ctc) if not pd.isna(ctc) else 0.0
            
            # Check if placement already exists
            stmt = select(Placement).where(
                Placement.student_id == student_id,
                Placement.company_id == company_id
            )
            result = await session.execute(stmt)
            if result.scalar_one_or_none():
                continue
                
            p = Placement(
                student_id=student_id,
                company_id=company_id,
                ctc_lpa=ctc_value,
                # could infer is_internship if a column exists
                is_internship=False 
            )
            session.add(p)
            
        print("Committing placements to database...")
        await session.commit()
    print("Placements import complete.")

if __name__ == "__main__":
    asyncio.run(main())
