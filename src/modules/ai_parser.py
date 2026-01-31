import os
import json
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("BonjukOps.AI")

class AIParser:
    """
    E-posta metinlerinden AI (Gemini) kullanarak veri ayıklayan servis.
    """
    def __init__(self):
        self._check_enabled()
        # Default to 2.5 flash as it is available for this key
        self.model_name = "gemini-2.5-flash"
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"

    def _check_enabled(self):
        """
        API anahtarını kontrol eder ve gerekirse yükler. 
        Streamlit açıkken .env güncellenirse diye dinamik kontrol sağlar.
        """
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            self.enabled = True
        else:
            self.enabled = False

    def parse_reservation(self, email_text: str):
        """
        E-posta metnini Gemini'ye gönderir ve JSON olarak ayıklar.
        """
        if not hasattr(self, 'enabled') or not self.enabled:
            load_dotenv() # .env'yi tekrar okumaya zorla
            self._check_enabled()

        if not self.enabled:
            return None

        prompt = f"""
        Aşağıdaki e-posta metnini oku ve Bonjuk Bay rezervasyon sistemimiz için gerekli bilgileri JSON formatında çıkar.
        Sadece JSON objesini döndür, başka açıklama yapma.
        
        İstenen alanlar:
        - guest_name (Ad Soyad)
        - check_in (YYYY-MM-DD formatında)
        - check_out (YYYY-MM-DD formatında)
        - pax (Kişi sayısı, tamsayı)
        - accommodation_type (Oda/Çadır tipi)
        - guest_language (tr veya en - EĞER 'Id Number' varsa veya 'nationality' Turkish ise KESİNLİKLE 'tr' seç. Sadece 'Passport Number' varsa ve Türkçe konuşmuyorsa 'en' seç.)
        - nationality (Turkish veya Foreign - ID varsa Turkish, Passport varsa Foreign)
        - missing_info (Eksik olan alanların listesi)

        E-posta Metni:
        ---
        {email_text}
        ---
        """

        try:
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }
            
            response = requests.post(
                f"{self.url}?key={self.api_key}",
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                # Gemini bazen markdown içinde döndürür, temizle
                raw_text = result['candidates'][0]['content']['parts'][0]['text']
                json_str = raw_text.strip().replace('```json', '').replace('```', '')
                return json.loads(json_str)
            else:
                logger.error(f"Gemini API Hatası ({response.status_code}): {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"AI Parsing Hatası: {e}")
            return None

    def generate_response(self, parsed_data: dict, template_type: str):
        """
        Ayrıştırılmış veriyi ve seçilen şablon tipini kullanarak AI ile yanıt üretir.
        """
        if not self.enabled:
            return "AI Devre Dışı."

        # Şablonları oku (Gerçek dünyada dosyadan okunmalı, şimdilik direkt prompt'a ekliyorum)
        templates_context = """
        Şablon 1 (Eksik Bilgi - TR):
        Sevgili {guest_name},
        
        Rezervasyon talebin harika görünüyor. Seni aramızda görmeyi çok isteriz.
        Size en uygun yerleşimi yapabilmemiz için ufak bir detaya ihtiyacımız var:
        👉 {missing_info}
        
        Bu bilgiyi bizimle paylaşırsan işlemlere hemen devam edebiliriz.
        Warm hugs! ✨

        Şablon 2 (Konfirmasyon - TR):
        Sevgili {guest_name},

        Bonjuk Bay'e ilgine teşekkür ederiz, sizi aramızda görmeyi çok isteriz.

        Referans olması için 2026 fiyat listemize ve konaklama seçeneklerimize aşağıdaki bağlantılardan ulaşabilirsin:
        
        2026 Fiyat Listesi:
        https://bonjukbay-my.sharepoint.com/personal/reservation_bonjukbay_com/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Freservation%5Fbonjukbay%5Fcom%2FDocuments%2FBerk%20Lenovo%20Desktop%2FBonjuk%20Bay%2025%20%2D%20Price%20List%2Epdf&parent=%2Fpersonal%2Freservation%5Fbonjukbay%5Fcom%2FDocuments%2FBerk%20Lenovo%20Desktop&ga=1
        
        Konaklama Seçenekleri:
        https://bonjukbay.com/accommodation.html

        {check_in} - {check_out} tarihleri arasındaki rezervasyonunu {accommodation_type} için opsiyonladık.

        Rezervasyonunu onaylamak için aşağıdaki hesap bilgilerimize ödeme göndermeni ve dekontu bizimle paylaşmanı rica ederiz.
        
        Kredi kartıyla ödemek istersen de aşağıdaki linki kullanabilirsin:
        [ÖDEME LINKI]

        Rezervasyonunu 24 saatliğine opsiyonluyoruz.

        Hesap Adı : GRANT ZAFER TURİZM İNŞAAT MADEN SANAYİ VE TİCARET LİMİTED ŞİRKETİ
        IBAN : TR490006701000000034479515
        SWIFT Kodu (EUR, USD) : YAPITRISXXX
        SWIFT Kodu (Diğer Döviz Cinsleri) : YAPITRISFEX
        Açıklama: {guest_name} / {check_in}

        2026 Update: Bu sezon ritmimizi biraz daha gündüze taşıyoruz. Hafta sonu 01:00’den sonra müzik olmayacak. Doğanın, dengenin ve anda kalmanın önceliklendiği; daha yumuşak, daha bilinçli ve daha sağlıklı bir Bonjuk deneyimine davetlisin!
        
        Warm hugs!
        """

        # Verileri önceden temizle (Python tarafında) - AI'ya bırakma
        raw_name = parsed_data.get('guest_name', 'Misafir')
        # Sadece ilk ismi al ve baş harfini büyüt (örn: ALPER YILMAZ -> Alper)
        first_name = raw_name.split()[0].title() if raw_name else "Misafir"
        
        # Prompt'a gidecek veriyi güncelle
        prompt_data = parsed_data.copy()
        prompt_data['guest_name'] = first_name

        prompt = f"""
        Aşağıdaki verileri kullanarak, Bonjuk Bay'in sıcak ve samimi dilinde bir yanıt taslağı oluştur.
        
        KESİN KURALLAR (Bunlara uymazsan sistem hata verir):
        1. Asla "Konu:" veya "Subject:" satırı ekleme.
        2. DOĞRUDAN "Sevgili {first_name}," ile başla. (İsim aynen bu şekilde yazılmalı).
        3. EMOJİ KULLANIMI YASAK: Metin içinde 🔗, 🙏, 💳, ⏳ gibi simgeler KESİNLİKLE kullanma.
        4. Sadece kapanışta 1 adet 🌞 veya ✨ kullanabilirsin. Başka emoji yasak.
        5. "{first_name}" ismini kullan, soyadı kullanma.
        
        Veriler:
        {json.dumps(prompt_data)}
        
        Şablon Bağlamı (Referans al):
        {templates_context}
        
        İstenen Yanıt Tipi: {template_type}
        """

        # Retry mekanizması
        max_retries = 3
        retry_delay = 5  # saniye

        for attempt in range(max_retries):
            try:
                payload = {
                    "contents": [
                        {
                            "parts": [
                                {"text": prompt}
                            ]
                        }
                    ]
                }
                
                response = requests.post(
                    f"{self.url}?key={self.api_key}",
                    headers={"Content-Type": "application/json"},
                    json=payload,
                    timeout=20
                )
                
                if response.status_code == 200:
                    result = response.json()
                    # Gemini bazen markdown içinde döndürür, temizle
                    raw_text = result['candidates'][0]['content']['parts'][0]['text']
                    if template_type == "parsing": # Sadece parsing için json temizliği yap
                         json_str = raw_text.strip().replace('```json', '').replace('```', '')
                         return json.loads(json_str)
                    return raw_text # Normal text döner

                elif response.status_code == 429:
                    if attempt < max_retries - 1:
                        import time
                        wait_time = retry_delay * (attempt + 1)
                        logger.warning(f"Rate limit (429). {wait_time}sn bekleniyor... (Deneme {attempt+1}/{max_retries})")
                        time.sleep(wait_time)
                        continue
                    else:
                        return "⚠️ Google AI Hız Sınırı Aşıldı (429). Lütfen daha sonra tekrar deneyin."
                else:
                    return f"Hata: {response.status_code}"
                    
            except Exception as e:
                return f"AI Hatası: {str(e)}"

# Singleton instance
ai_parser = AIParser()
