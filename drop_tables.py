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
    print("Dropping conflicting tables...")
    try:
        conn.execute(sqlalchemy.text("DROP TABLE IF EXISTS minor_degrees CASCADE;"))
        conn.execute(sqlalchemy.text("DROP TABLE IF EXISTS offers CASCADE;"))
        conn.execute(sqlalchemy.text("DROP TABLE IF EXISTS placements CASCADE;"))
        conn.execute(sqlalchemy.text("DROP TABLE IF EXISTS companies CASCADE;"))
        conn.execute(sqlalchemy.text("DROP TABLE IF EXISTS students CASCADE;"))
        conn.commit()
        print("Success.")
    except Exception as e:
        print(f"Error: {e}")
