import asyncio
import sys
from sqlalchemy.future import select
from core.db import AsyncSessionLocal, Base, engine
from models.user import User
from models.role import Role
from core.auth_utils import hash_password

async def create_roles_and_users():
    async with AsyncSessionLocal() as session:
        print("Checking roles...")
        
        # 1. Ensure Roles Exist
        roles_to_create = ["admin", "faculty", "student", "placement_officer"]
        role_map = {}
        
        for role_name in roles_to_create:
            result = await session.execute(select(Role).where(Role.name == role_name))
            role = result.scalar_one_or_none()
            if not role:
                print(f"Creating role: {role_name}")
                role = Role(name=role_name)
                session.add(role)
                await session.commit()
                await session.refresh(role)
            else:
                print(f"Role exists: {role_name} (ID: {role.id})")
            role_map[role_name] = role.id
        
        print(f"Role Map: {role_map}")

        # 2. Create Test Users
        users_to_create = [
            {"email": "admin@vnr.edu.in", "password": "admin", "role": "admin"},
            {"email": "faculty@vnr.edu.in", "password": "faculty123", "role": "faculty"},
            {"email": "student@vnr.edu.in", "password": "student123", "role": "student"},
            {"email": "po@vnr.edu.in", "password": "po123", "role": "placement_officer"},
        ]

        print("\nChecking users...")
        for user_data in users_to_create:
            result = await session.execute(select(User).where(User.email == user_data["email"]))
            user = result.scalar_one_or_none()
            
            if not user:
                print(f"Creating user: {user_data['email']}")
                new_user = User(
                    email=user_data["email"],
                    password=hash_password(user_data["password"]), # Hash the password!
                    role_id=role_map[user_data["role"]]
                )
                session.add(new_user)
            else:
                print(f"User exists: {user_data['email']}. Updating password...")
                user.password = hash_password(user_data["password"])
                session.add(user)
        
        await session.commit()
        print("\nDone! Test users ready.")

if __name__ == "__main__":
    # Ensure invalid event loop policy doesn't crash on Windows
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(create_roles_and_users())
