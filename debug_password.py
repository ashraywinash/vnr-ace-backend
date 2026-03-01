import asyncio
import sys
from sqlalchemy.future import select
from core.db import AsyncSessionLocal
from models.user import User
from core.auth_utils import verify_password, hash_password

async def verify_student_password():
    email = "student@vnr.edu.in"
    password = "student123"
    
    with open("debug_output.txt", "w", encoding="utf-8") as f:
        f.write(f"Checking pass for: {email}\n")
        
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            
            if not user:
                f.write("User NOT found!\n")
                return
                
            f.write(f"User Found. ID: {user.id}\n")
            f.write(f"Stored Hash: {repr(user.password)}\n")
            
            # Test Verification
            is_valid = verify_password(password, user.password)
            f.write(f"Verify '{password}' against Stored Hash: {is_valid}\n")
            
            # Test Hashing
            new_hash = hash_password(password)
            f.write(f"New Hash of '{password}': {new_hash}\n")
            
            # Verify New Hash
            is_valid_new = verify_password(password, new_hash)
            f.write(f"Verify '{password}' against New Hash: {is_valid_new}\n")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify_student_password())
