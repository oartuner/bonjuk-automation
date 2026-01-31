import logging

logger = logging.getLogger("BonjukOps.Reservation")

def validate_reservation(data: dict):
    """
    Rezervasyon verilerini doğrular ve eksik alanları döner.
    """
    required_fields = {
        "guest_name": "Ad Soyad",
        "check_in": "Giriş Tarihi",
        "check_out": "Çıkış Tarihi",
        "pax": "Kişi Sayısı",
        "accommodation_type": "Konaklama Tipi"
    }
    
    missing = []
    for field, label in required_fields.items():
        if not data.get(field):
            missing.append(label)
            
    return {
        "is_valid": len(missing) == 0,
        "missing_fields": missing,
        "summary": f"Eksik alanlar: {', '.join(missing)}" if missing else "Veriler tam."
    }

def generate_welcome_email(guest_name: str, missing_fields: list):
    """
    Eksik alanlara göre hoşgeldin/bilgi isteme e-postası taslağı oluşturur.
    """
    if not missing_fields:
        return f"Merhaba {guest_name}, talebinizi aldık! Teklifimizi hazırlıyoruz. 🧿"
    
    fields_str = ", ".join(missing_fields)
    return (f"Merhaba {guest_name}, talebiniz için teşekkürler! "
            f"Size en uygun teklifi hazırlayabilmemiz için şu bilgiler eksik görünüyor: {fields_str}. "
            f"Bunları tamamlayabilir misiniz? 🧿")
