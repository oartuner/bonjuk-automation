import os
from dotenv import load_dotenv
load_dotenv()

host = os.getenv("EMAIL_HOST")
user = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")

print(f"HOST: {host}")
print(f"USER: {user}")
print(f"PASS: {'***' if password else 'MISSING'}")

if not all([host, user, password]):
    print("CONFIG MISSING!")
else:
    print("CONFIG OK!")
