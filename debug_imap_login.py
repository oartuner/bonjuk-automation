import imaplib
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("EMAIL_HOST")
user = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")

print(f"Server: {host}")
print(f"User: {user}")

try:
    mail = imaplib.IMAP4_SSL(host)
    print("Connecting to server...")
    mail.login(user, password)
    print("✅ AUTH SUCCESS!")
    mail.logout()
except Exception as e:
    print(f"❌ ERROR: {e}")
