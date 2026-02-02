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

# Helper function to read from env or streamlit secrets
def get_setting(key, default=None):
    """
    Önce environment variable'ı kontrol eder, yoksa Streamlit secrets'a bakar.
    Bu sayede hem yerelde (.env) hem de Streamlit Cloud'da çalışır.
    """
    # 1. Environment Variable (Yerel .env dosyasından)
    val = os.getenv(key)
    if val:
        return val
    
    # 2. Streamlit Secrets (Cloud)
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except:
        pass
        
    return default


# Basit ve Etkili Config Sınıfı
class Config:
    @staticmethod
    def get(key, default=None):
        """Değeri env veya st.secrets'tan okur"""
        # 1. Environment variable
        val = os.getenv(key)
        if val:
            return val
        
        # 2. Streamlit secrets
        try:
            import streamlit as st
            if key in st.secrets:
                return st.secrets[key]
        except:
            pass
        
        return default
    
    # Değerleri dinamik olarak okuyoruz
    @property
    def EMAIL_HOST(self):
        return self.get("EMAIL_HOST")
    
    @property
    def EMAIL_PORT(self):
        return int(self.get("EMAIL_PORT", "993"))
    
    @property
    def EMAIL_USER(self):
        return self.get("EMAIL_USER")
    
    @property
    def EMAIL_PASS(self):
        return self.get("EMAIL_PASS")
    
    @property
    def GEMINI_API_KEY(self):
        return self.get("GEMINI_API_KEY")

    def validate_email_config(self):
        """Email ayarlarının eksiksiz olup olmadığını kontrol eder."""
        if not all([self.EMAIL_HOST, self.EMAIL_USER, self.EMAIL_PASS]):
            logger.error("❌ E-posta ayarları EKSİK")
            logger.error(f"HOST: {self.EMAIL_HOST}, USER: {self.EMAIL_USER}, PASS: {'***' if self.EMAIL_PASS else None}")
            return False
        logger.info(f"✅ Email config OK: {self.EMAIL_USER}")
        return True

# Global config instance
config = Config()

