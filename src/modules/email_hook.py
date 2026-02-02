import logging
from imap_tools import MailBox, AND
from src.config import config

logger = logging.getLogger("BonjukOps.Email")

class EmailHook:
    """
    E-posta kutusuna bağlanıp rezervasyon maillerini yakalayan servis.
    """
    def __init__(self):
        self.enabled = config.validate_email_config()
        if self.enabled:
            logger.info(f"EmailHook başlatılıyor: {config.EMAIL_USER} ({config.EMAIL_HOST})")

    def fetch_unseen_emails(self, limit=5):
        """
        Okunmamış son mailleri getirir.
        """
        if not self.enabled:
            logger.warning("EmailHook devre dışı, e-posta kontrolü yapılamıyor.")
            return []

        emails = []
        try:
            # Bağlantı kur
            logger.info("IMAP sunucusuna bağlanılıyor...")
            with MailBox(config.EMAIL_HOST).login(config.EMAIL_USER, config.EMAIL_PASS) as mailbox:
                logger.info("✅ Bağlantı başarılı! Klasör taranıyor...")
                
                # 'UNSEEN' mailleri ara
                # Not: Bazen tarih sırası karışabilir, reverse=True en yenileri getirir.
                for msg in mailbox.fetch(AND(seen=False), limit=limit, reverse=True):
                    emails.append({
                        "subject": msg.subject,
                        "from": msg.from_,
                        "date": msg.date_str, # Daha okunaklı tarih formatı
                        "body": msg.text or msg.html,
                        "id": msg.uid
                    })
                    
            logger.info(f"📬 {len(emails)} adet okunmamış e-posta bulundu.")
            return emails
            
        except Exception as e:
            logger.error(f"❌ E-posta çekme hatası: {e}")
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
