import sys
import os
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")

if db_url and db_url.startswith("postgresql+asyncpg://"):
    db_url = db_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://")

print("Testing database URL (sync):", db_url)

try:
    engine = sqlalchemy.create_engine(db_url)
    with engine.connect() as conn:
        print("Successfully connected dynamically!")
        res = conn.execute(sqlalchemy.text("SELECT 'connection works'")).scalar()
        print("Query output:", res)
        sys.exit(0)
except Exception as e:
    print(f"Failed: {e}")
    sys.exit(1)
