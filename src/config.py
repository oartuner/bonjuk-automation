import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Logger kurulumu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BonjukOps.Config")

# Proje Kök Dizinini Bul (src/config.py -> src -> root)
BASE_DIR = Path(__file__).resolve().parent.parent

# .env dosyasını yükle
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(env_path, override=True)
    logger.info(f".env yüklendi: {env_path}")
else:
    logger.warning(f".env BULUNAMADI: {env_path}")

# Konfigürasyon Sınıfı
class Config:
    # App
    ENV = os.getenv("APP_ENV", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    TIMEZONE = os.getenv("TIMEZONE", "Europe/Istanbul")
    
    # Email (Gmail/Outlook)
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 993))
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    
    # AI
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Supabase (Optional)
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    @classmethod
    def validate_email_config(cls):
        """Email ayarlarının eksiksiz olup olmadığını kontrol eder."""
        if not all([cls.EMAIL_HOST, cls.EMAIL_USER, cls.EMAIL_PASS]):
            logger.error("❌ E-posta ayarları EKSİK! Lütfen .env dosyasını kontrol edin.")
            return False
        return True

# Global erişim için
config = Config()
