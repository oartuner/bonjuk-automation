import os
import logging
import requests
from dotenv import load_dotenv
from datetime import datetime

# Yapılandırmayı yükle
load_dotenv()

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("BonjukOps")

def trigger_n8n_webhook(workflow_data: dict):
    """
    n8n webhook tetikleyicisi.
    """
    webhook_url = os.getenv("N8N_WEBHOOK_URL")
    if not webhook_url:
        logger.error("HATA: N8N_WEBHOOK_URL tanımlanmamış.")
        return False
    
    try:
        response = requests.post(webhook_url, json=workflow_data, timeout=10)
        response.raise_for_status()
        logger.info(f"BAŞARILI: n8n webhook tetiklendi. Durum: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"HATA: n8n tetiklenirken sorun oluştu: {e}")
        return False

def check_system_health():
    """
    Sistem sağlığını kontrol eder ve n8n'e raporlar.
    """
    logger.info("📡 Bonjuk Sistem Kontrolü Başlatıldı...")
    
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "service": "bonjuk-ops",
        "region": "Türkiye",
        "timezone": "Europe/Istanbul"
    }
    
    # n8n'e rapor gönder
    success = trigger_n8n_webhook(health_data)
    
    if success:
        logger.info("✅ Bonjuk Operasyonel Otomasyon Hazır ve Nazır! 🧿")
    else:
        logger.warning("⚠️ Sistem sağlıklı ancak n8n raporu gönderilemedi.")

if __name__ == "__main__":
    check_system_health()
