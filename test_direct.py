import asyncio
from core.db import engine, get_db
from models.company_prep import CompanyPrepQuestion
from sqlalchemy import select

async def test():
    async for db in get_db():
        stmt = select(CompanyPrepQuestion).where(
            CompanyPrepQuestion.company_name.ilike("Google")
        )
        try:
            result = await db.execute(stmt)
            record = result.scalars().first()
            if record:
                print({"company": record.company_name, "questions": record.questions})
            else:
                print("No record")
        except Exception as e:
            print(f"Error executing statement: {e}")
        break

if __name__ == '__main__':
    asyncio.run(test())
