import os
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("BonjukOps.DB")

class DatabaseService:
    """
    Supabase REST API'sini doğrudan (requests ile) kullanan hafif servis.
    Kütüphane bağımlılığını ve kurulum hatalarını ortadan kaldırır.
    """
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if self.url and self.key:
            # URL'yi temizle (sonda / varsa kaldır)
            self.url = self.url.rstrip('/')
            self.headers = {
                "apikey": self.key,
                "Authorization": f"Bearer {self.key}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            }
            logger.info("Supabase REST API bağlantısı hazır.")
        else:
            self.url = None
            logger.warning("Supabase URL veya KEY eksik. Veritabanı devredışı.")

    def save_reservation(self, data: dict):
        """
        Rezervasyonu 'reservations' tablosuna POST eder.
        """
        if not self.url:
            return False, "Veritabanı yapılandırılmamış."

        # create_at ekle
        data["created_at"] = datetime.now().isoformat()

        try:
            endpoint = f"{self.url}/rest/v1/reservations"
            response = requests.post(endpoint, headers=self.headers, json=data, timeout=10)
            
            if response.status_code in [200, 201, 204]:
                logger.info(f"Başarılı: {data.get('guest_name')} kaydedildi.")
                return True, "Başarıyla kaydedildi."
            else:
                logger.error(f"Supabase Hatası ({response.status_code}): {response.text}")
                return False, f"Supabase Hatası: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Bağlantı Hatası: {e}")
            return False, f"Bağlantı Hatası: {str(e)}"

    def get_recent_reservations(self, limit=5):
        """
        Son rezervasyonları çeker.
        """
        if not self.url:
            return []

        try:
            # Sorgu formatı: ?select=*&order=created_at.desc&limit=5
            endpoint = f"{self.url}/rest/v1/reservations?select=*&order=created_at.desc&limit={limit}"
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Veri Çekme Hatası ({response.status_code}): {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Veri Çekme Hatası: {e}")
            return []

# Singleton instance
db_service = DatabaseService()
