import asyncio
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.db import AsyncSessionLocal
from models.company import Company
from sqlalchemy import select

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
        
    if 'Company Name' not in df.columns:
        print("Required column 'Company Name' not found.")
        return
        
    # Get distinct company names
    unique_companies = df['Company Name'].dropna().unique()
    
    async with AsyncSessionLocal() as session:
        for comp_name in unique_companies:
            name_str = str(comp_name).strip()
            
            # Check if exists
            stmt = select(Company).where(Company.name == name_str)
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if existing:
                continue
                
            company = Company(name=name_str)
            session.add(company)
            
        print("Committing companies to database...")
        await session.commit()
    print("Company import complete.")

if __name__ == "__main__":
    asyncio.run(main())
