import asyncio
import sys
from sqlalchemy.future import select
from core.db import AsyncSessionLocal
from models.user import User

async def check_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(f"Total Users: {len(users)}")
        for user in users:
            print(f"User: {user.email}, Role ID: {user.role_id}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(check_users())
