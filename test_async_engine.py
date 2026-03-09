import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()
db_url = os.getenv("DATABASE_URL")
if db_url and db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

async def test_db():
    print("Testing async connection...")
    try:
        # According to some docs, connect_args is passed to asyncpg.connect
        # Wait, the pool argument in sqlalchemy is `prepared_statement_cache_size=0` for psycopg2/pg8000.
        engine = create_async_engine(
            db_url,
            connect_args={
                "statement_cache_size": 0,    # asyncpg kwarg
                "prepared_statement_cache_size": 0, # asyncpg kwarg
                "ssl": "require"
            }
        )
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            print("Successfully connected and executed query with connect_args only.")
    except Exception as e:
        print(f"Failed with connect_args: {e}")

asyncio.run(test_db())
