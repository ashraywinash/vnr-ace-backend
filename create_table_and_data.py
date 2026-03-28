import asyncio
from core.db import engine
from models.company_prep import CompanyPrepQuestion
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async def run():
    # Only create the new table
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: CompanyPrepQuestion.__table__.create(sync_conn, checkfirst=True))
        
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        # Add dummy data
        dummy = CompanyPrepQuestion(
            company_name="Google",
            experiences=["The interview was highly focused on Graph algorithms and system design..."],
            questions=["Find the shortest path in an unweighted graph.", "Design a scalable URL shortener."]
        )
        session.add(dummy)
        await session.commit()
    print("Table created and dummy data added successfully.")

if __name__ == '__main__':
    asyncio.run(run())
