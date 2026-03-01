from core.auth_utils import hash_password, verify_password

password = "student123"
print(f"Testing password: {password}")

hashed = hash_password(password)
print(f"Generated Hash: {hashed}")
print(f"Hash Length: {len(hashed)}")

is_valid = verify_password(password, hashed)
print(f"Verification Result: {is_valid}")
