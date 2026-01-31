import os
import requests
from dotenv import load_dotenv

# Load env execution
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

print(f"API Key Loaded: {bool(API_KEY)}")
if API_KEY:
    print(f"API Key First 4 chars: {API_KEY[:4]}")

email_text = """Dear ALPER, Your reservation request has reached us. 
Reservation Details; Guest Name: ALPER YILMAZ 
Id Number: 25052200208 Passport Number: 
Social Link: alperr_yz 
Room Type: Sea Front Room BedType: Double Bed 
Check-In: 06.08.2026 Check-Out: 10.08.2026 Pax: 2 
Message: Could you please reserve for us for two people Sea Front Room for dance weekend btw 6 August- 10 August."""

prompt = f"""
        Aşağıdaki e-posta metnini oku ve Bonjuk Bay rezervasyon sistemimiz için gerekli bilgileri JSON formatında çıkar.
        Sadece JSON objesini döndür, başka açıklama yapma.
        
        İstenen alanlar:
        - guest_name (Ad Soyad)
        - check_in (YYYY-MM-DD formatında)
        - check_out (YYYY-MM-DD formatında)
        - pax (Kişi sayısı, tamsayı)
        - accommodation_type (Oda/Çadır tipi)
        - guest_language (tr veya en - İçerik diline veya ID/Passport alanına göre belirle)
        - nationality (Turkish veya Foreign - ID varsa Turkish, Passport varsa Foreign)
        - missing_info (Eksik olan alanların listesi)

        E-posta Metni:
        ---
        {email_text}
        ---
        """

payload = {
    "contents": [
        {
            "parts": [
                {"text": prompt}
            ]
        }
    ]
}

print(f"Sending request to Gemini ({URL})...")
try:
    response = requests.post(
        f"{URL}?key={API_KEY}",
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=20
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print(f"Error Response: {response.text}")
    else:
        print("Success!")
        # print(response.json())
        print(response.json()['candidates'][0]['content']['parts'][0]['text'])

except Exception as e:
    print(f"Exception: {e}")
