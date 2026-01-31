import os
import logging
from imap_tools import MailBox, AND
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("BonjukOps.Email")

class EmailHook:
    """
    E-posta kutusuna bağlanıp rezervasyon maillerini yakalayan servis.
    """
    def __init__(self):
        self.host = os.getenv("EMAIL_HOST")
        port_val = os.getenv("EMAIL_PORT")
        self.port = int(port_val) if port_val and port_val.isdigit() else 993
        self.user = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASS")
        
        if not all([self.host, self.user, self.password]):
            logger.warning("E-posta konfigürasyonu eksik. EmailHook devre dışı.")
            self.enabled = False
        else:
            self.enabled = True
            logger.info(f"EmailHook hazır: {self.user}")

    def fetch_unseen_emails(self, limit=5):
        """
        Okunmamış son mailleri getirir.
        """
        if not self.enabled:
            return []

        emails = []
        try:
            with MailBox(self.host).login(self.user, self.password) as mailbox:
                # 'UNSEEN' olan ve 'Reservation' içeren mailleri ara
                for msg in mailbox.fetch(AND(seen=False), limit=limit, reverse=True):
                    emails.append({
                        "subject": msg.subject,
                        "from": msg.from_,
                        "date": msg.date,
                        "body": msg.text or msg.html,
                        "id": msg.uid
                    })
            return emails
        except Exception as e:
            logger.error(f"E-posta çekme hatası: {e}")
            return []

    def get_sample_email(self):
        """
        Kullanıcının paylaştığı .eml dosyasındaki gerçek veriyi simüle eder.
        """
        return {
            "subject": "Fw: Your New Reservation Request (3111)",
            "from": "Alper Yılmaz <alper.ymaz@yahoo.com.tr>",
            "date": "2026-01-27 13:20:00",
            "body": """Dear ALPER, Your reservation request has reached us. 
            Reservation Details; Guest Name: ALPER YILMAZ 
            Id Number: 25052200208 Passport Number: 
            Social Link: alperr_yz 
            Room Type: Sea Front Room BedType: Double Bed 
            Check-In: 06.08.2026 Check-Out: 10.08.2026 Pax: 2 
            Message: Could you please reserve for us for two people Sea Front Room for dance weekend btw 6 August- 10 August.""",
            "id": "SIM-3111"
        }

# Singleton instance
email_hook = EmailHook()
