import logging
import json
import requests
from src.config import config
from src.modules.content import get_event_for_date, TEMPLATES

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
        - has_children (Boolean - Metinde çocuk, bebek, kids, child kavramları geçiyor mu?)
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
                raw_text = result['candidates'][0]['content']['parts'][0]['text']
                json_str = raw_text.strip().replace('```json', '').replace('```', '')
                parsed = json.loads(json_str)

                # Event Kontrolü (Content Modülünden) - YENİ
                if 'check_in' in parsed and parsed['check_in']:
                    event = get_event_for_date(parsed['check_in'])
                    if event:
                        parsed['event_name'] = event['name']
                        parsed['event_fee'] = event.get('fee')
                        parsed['event_kids_allowed'] = event.get('kids_allowed', False)
                    else:
                        parsed['event_name'] = None
                        parsed['event_fee'] = None
                        parsed['event_kids_allowed'] = False
                
                return parsed
            else:
                logger.error(f"Gemini API Hatası ({response.status_code}): {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"AI Parsing Hatası: {e}")
            return None

    def generate_response(self, parsed_data: dict, template_type: str):
        """
        Ayrıştırılmış veriyi ve seçilen şablon tipini kullanarak AI ile yanıt üretir.
        GÜNCELLEME: Artık manuel template yerine content.py'deki standart şablonları kullanır.
        """
        try:
            first_name = parsed_data.get('guest_name', 'Misafir').split()[0].title()
            lang_code = parsed_data.get('guest_language', 'tr')
            if lang_code not in ['tr', 'en']: lang_code = 'tr'

            # Şablon Seçimi
            # template_type değerini map'le
            tpl_key = "welcome"
            if "Konfirmasyon" in template_type or "Confirmation" in template_type:
                tpl_key = "confirm_payment"
            elif "Eksik" in template_type or "Missing" in template_type:
                # Eksik bilgide özel logic yok, direkt eksik alanları yazıyoruz
                # Ama content.py'de buna özel şablon yoksa basitçe oluşturabiliriz
                # Hatta app.py artık manuel şablon kullanıyor, burası AI production için.
                # Şimdilik basitçe pass geçip context'e ekleyelim.
                pass 
                
            # Content.py içindeki şablonu al
            # NOT: Kullanıcı AI'nın template'i doldurmasını istiyor, direkt string format değil.
            # O yüzden template'i prompt'a context olarak vereceğiz.
            
            target_template = TEMPLATES[lang_code].get(tpl_key, TEMPLATES[lang_code]["welcome"])
            
            # Çocuk Kontrolü & Reddetme
            if parsed_data.get('has_children') and not parsed_data.get('event_kids_allowed', False):
                # Çocuk var ama etkinlik izin vermiyor -> Reddet
                target_template = TEMPLATES[lang_code]["rejection_kids"]
                template_type = "REJECTION (Child Policy)"
            
            # Event Fee Bilgisi
            event_fee_info = ""
            if parsed_data.get('event_fee'):
                if lang_code == 'tr':
                    event_fee_info = f"Bu etkinlik için ayrıca kişi başı {parsed_data['event_fee']} katılım ücreti bulunmaktadır."
                else:
                    event_fee_info = f"Please note there is an additional participation fee of {parsed_data['event_fee']} per person for this event."
            
            # Prompt hazırlığı
            prompt = f"""
            GÖREV: Aşağıdaki rezervasyon verilerini kullanarak, ekteki ŞABLONU doldur.
            
            KURALLAR:
            1. Şablondaki metne sadık kal. Sadece {{brackets}} içindeki değişkenleri doldur.
            2. Eğer şablonda {{event_fee_info}} varsa, verilerdeki 'event_fee_info' metnini oraya koy. Yoksa boş bırak.
            3. Asla "Konu:" satırı ekleme.
            4. İsim olarak sadece '{first_name}' kullan.
            5. Emoji ekleme (Şablondakiler kalsın).
            
            VERİLER:
            {json.dumps(parsed_data, ensure_ascii=False)}
            Special 'event_fee_info' text: "{event_fee_info}"

            KULLANILACAK ŞABLON (Bunu doldur):
            ---
            {target_template}
            ---
            """

            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            
            # ... (Standart request kodu) ...
            response = requests.post(f"{self.url}?key={self.api_key}", headers={"Content-Type": "application/json"}, json=payload, timeout=20)
            
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"Hata: {response.status_code}"

        except Exception as e:
             return f"AI Yanıt Üretme Hatası: {e}"

# Singleton instance
ai_parser = AIParser()
