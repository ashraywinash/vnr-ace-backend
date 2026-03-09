import sys
import os
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")
if db_url and db_url.startswith("postgresql+asyncpg://"):
    db_url = db_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://")

engine = sqlalchemy.create_engine(db_url)
with engine.connect() as conn:
    print("Listing columns in 'students' table:")
    try:
        res = conn.execute(sqlalchemy.text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'students';
        """))
        for row in res:
            print(row[0], ":", row[1])
    except Exception as e:
        print(f"Error: {e}")
