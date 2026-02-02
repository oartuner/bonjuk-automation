import os
import logging
from imap_tools import MailBox, AND
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

host = os.getenv("EMAIL_HOST")
user = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")

print(f"Bağlanılıyor: {host} (Kullanıcı: {user})")

try:
    with MailBox(host).login(user, password) as mailbox:
        print("✅ Giriş başarılı!")
        
        # Klasörleri listele (Bazı hesaplarda 'INBOX' dışında isimler olabilir)
        print("\n--- Klasör Listesi ---")
        for folder in mailbox.folder.list():
            print(f"- {folder.name}")
            
        # Okunmamış mailleri say
        print("\n--- Okunmamış Mailler (Son 5) ---")
        unseen_count = 0
        for msg in mailbox.fetch(AND(seen=False), limit=5, reverse=True):
            unseen_count += 1
            print(f"Konu: {msg.subject} | Kimden: {msg.from_}")
            
        if unseen_count == 0:
            print("HİÇ OKUNMAMIŞ MAİL BULUNAMADI.")
            
except Exception as e:
    print(f"❌ BAĞLANTI HATASI: {e}")
