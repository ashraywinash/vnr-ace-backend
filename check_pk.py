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
    print("Listing primary keys for 'students':")
    try:
        res = conn.execute(sqlalchemy.text("""
            SELECT a.attname, format_type(a.atttypid, a.atttypmod) AS data_type
            FROM   pg_index i
            JOIN   pg_attribute a ON a.attrelid = i.indrelid
                                 AND a.attnum = ANY(i.indkey)
            WHERE  i.indrelid = 'students'::regclass
            AND    i.indisprimary;
        """))
        for row in res:
            print(row[0], ":", row[1])
    except Exception as e:
        print(f"Error: {e}")
