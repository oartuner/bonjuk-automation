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
    # Helper to get env or secret
    @staticmethod
    def get_setting(key, default=None):
        # 1. Önce Environment Variable'a bak (Yerel .env)
        val = os.getenv(key)
        if val:
            return val
        
        # 2. Yoksa Streamlit Secrets'a bak (Cloud)
        try:
            import streamlit as st
            if key in st.secrets:
                return st.secrets[key]
        except:
            pass
            
        return default

    # App
    ENV = os.getenv("APP_ENV", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Email (Gmail/Outlook)
    EMAIL_HOST = get_setting.__func__("EMAIL_HOST")
    EMAIL_PORT = int(get_setting.__func__("EMAIL_PORT", 993))
    EMAIL_USER = get_setting.__func__("EMAIL_USER")
    EMAIL_PASS = get_setting.__func__("EMAIL_PASS")
    
    # AI
    GEMINI_API_KEY = get_setting.__func__("GEMINI_API_KEY")

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
