def determine_vehicle_type(pax: int):
    """
    Yolcu sayısına göre araç tipini belirler.
    """
    if pax <= 3:
        return "Taksi (Standard Sedan)"
    elif pax <= 7:
        return "Van (Vito / Caravelle)"
    elif pax <= 13:
        return "Sprinter (Minibüs)"
    else:
        return "Çoklu Araç Gerekli"

def get_transfer_price_estimate(route: str, pax: int):
    """
    Güzergah ve yolcu sayısına göre tahmini fiyat döner.
    (Not: Gerçekte bir veritabanı veya dosyadan okunmalı)
    """
    prices = {
        "Dalaman-Bonjuk": {"Taksi": 2500, "Van": 3500, "Sprinter": 4500},
        "Bodrum-Bonjuk": {"Taksi": 4500, "Van": 6000, "Sprinter": 8000}
    }
    
    vehicle = determine_vehicle_type(pax).split(" (")[0]
    route_prices = prices.get(route)
    
    if route_prices:
        return route_prices.get(vehicle, "Fiyat sorunuz")
    return "Fiyat sorunuz (Medusa Transfer)"

def generate_supplier_order(guest_name: str, route: str, flight_info: str, pax: int, phone: str):
    """
    Tedarikçi için iş emri metni oluşturur.
    """
    vehicle = determine_vehicle_type(pax)
    return f"""
🏨 **BONJUK BAY TRANSFER İŞ EMRİ**

**Misafir:** {guest_name}
**Telefon:** {phone}
**Güzergah:** {route}
**Uçuş Bilgisi:** {flight_info}
**Yolcu Sayısı:** {pax}
**Araç Tipi:** {vehicle}

*Lütfen onay bekleyiniz.*
"""
