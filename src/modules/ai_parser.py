import logging
import json
import requests
from src.config import config

logger = logging.getLogger("BonjukOps.AI")

class AIParser:
    """
    E-posta metinlerinden AI (Gemini) kullanarak veri ayıklayan servis.
    """
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        # Kullanıcının API anahtarına tanımlı tek model 'gemini-2.5-flash'.
        self.model_name = "gemini-2.5-flash"
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"
        
        if self.api_key:
            self.enabled = True
        else:
            self.enabled = False
            logger.warning("GEMINI_API_KEY eksik, AI devre dışı.")

    def parse_reservation(self, email_text: str):
        """
        E-posta metnini Gemini'ye gönderir ve JSON olarak ayıklar.
        """
        if not self.enabled:
            # Config'den tekrar kontrol et (runtime update ihtimaline karşı opsiyonel)
            if config.GEMINI_API_KEY:
                self.api_key = config.GEMINI_API_KEY
                self.enabled = True

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
        - special_requests (Özel istekler, notlar, mesaj - varsa doğum günü pastası, erken check-in vb.)
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
        https://bit.ly/Bonjukbay_FiyatListesi
        
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
                    
                    if template_type == "parsing": 
                         # JSON temizliği (Markdown bloklarını kaldır)
                         json_str = raw_text.strip().replace('```json', '').replace('```', '')
                         return json.loads(json_str)

                    return raw_text # Normal text döner

                elif response.status_code == 429:
                    logger.warning(f"Rate limit hit. Waiting {attempt+1}")
                    continue
                else:
                    error_msg = f"API Hatası: {response.status_code} - {response.text}"
                    print(error_msg) # Terminalde görmek için
                    logger.error(error_msg)
                    return f"Hata: {response.status_code}"
                    
            except Exception as e:
                error_msg = f"AI Hatası Exception: {str(e)}"
                print(error_msg)
                logger.error(error_msg)
                return f"AI Hatası: {str(e)}"

# Singleton instance
ai_parser = AIParser()
