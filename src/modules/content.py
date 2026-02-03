from datetime import datetime

# 2026 Event Calendar
# Format: "YYYY-MM-DD": {"name": "Event Name", "fee": "XX Euro", "kids_allowed": False}
# We will use a function to check ranges

EVENT_CALENDAR = [
    # Nisan - Mayıs
    {"start": "2026-04-23", "end": "2026-04-27", "name": "TBA", "fee": None},
    {"start": "2026-04-30", "end": "2026-05-04", "name": "Opening", "fee": None},
    {"start": "2026-05-06", "end": "2026-05-11", "name": "Eldium meets Bonjuk", "fee": None},
    {"start": "2026-05-14", "end": "2026-05-19", "name": "Forever Young", "fee": None},
    {"start": "2026-05-21", "end": "2026-05-24", "name": "Eda Anjel Wedding", "fee": None},
    {"start": "2026-05-25", "end": "2026-06-01", "name": "Bayram Fest", "fee": None},
    
    # Haziran
    {"start": "2026-06-04", "end": "2026-06-08", "name": "Seren Birthday + Project Heart", "fee": None},
    {"start": "2026-06-08", "end": "2026-06-15", "name": "Sharamania", "fee": None},
    {"start": "2026-06-18", "end": "2026-06-22", "name": "Roro", "fee": None},
    {"start": "2026-06-25", "end": "2026-06-29", "name": "Bonjuk Burn", "min_stay": 4, "fee": None},
    
    # Temmuz
    {"start": "2026-07-02", "end": "2026-07-06", "name": "The Muse Yoga", "fee": None},
    {"start": "2026-07-09", "end": "2026-07-13", "name": "Cirque Vortex", "fee": None},
    {"start": "2026-07-15", "end": "2026-07-20", "name": "Inner & Outer Journey", "fee": None},
    {"start": "2026-07-21", "end": "2026-07-26", "name": "The One Wellness", "fee": None},
    {"start": "2026-07-26", "end": "2026-07-30", "name": "Kids Week I", "kids_allowed": True, "fee": "100 Euro"},
    {"start": "2026-07-30", "end": "2026-08-03", "name": "Mayan Warrior", "fee": None},
    
    # Ağustos
    {"start": "2026-08-06", "end": "2026-08-10", "name": "Dance Weekend", "min_stay": 4, "fee": None},
    {"start": "2026-08-12", "end": "2026-08-16", "name": "Into the Light", "fee": None},
    {"start": "2026-08-16", "end": "2026-08-20", "name": "Kids Week II", "kids_allowed": True, "fee": "100 Euro"},
    {"start": "2026-08-27", "end": "2026-08-31", "name": "Victory", "fee": None},
    
    # Eylül - Ekim - Kasım
    {"start": "2026-09-17", "end": "2026-09-21", "name": "Necibe & Friends", "fee": None},
    {"start": "2026-09-24", "end": "2026-09-28", "name": "Love Weekend", "min_stay": 4, "fee": None},
    {"start": "2026-10-12", "end": "2026-10-19", "name": "I Am You", "fee": None},
    {"start": "2026-10-22", "end": "2026-10-26", "name": "Lukas Wedding", "fee": None},
    {"start": "2026-10-29", "end": "2026-11-02", "name": "Closing", "fee": None},
]

def get_event_for_date(check_in_date_str):
    """
    Verilen tarihe denk gelen etkinliği döndürür.
    Args:
        check_in_date_str (str): 'YYYY-MM-DD' formatında tarih.
    Returns:
        dict: Etkinlik detayları veya None
    """
    try:
        check_in = datetime.strptime(check_in_date_str, "%Y-%m-%d").date()
        for event in EVENT_CALENDAR:
            start = datetime.strptime(event["start"], "%Y-%m-%d").date()
            end = datetime.strptime(event["end"], "%Y-%m-%d").date()
            if start <= check_in <= end:
                return event
    except Exception as e:
        return None
    return None

# Email Templates
TEMPLATES = {
    "tr": {
        "welcome": """Sevgili {first_name},

Bonjuk Bay'e ilgine teşekkür ederiz, seni aramızda görmeyi çok isteriz.

Referans olması için 2026 fiyat listemize buradan ve konaklama seçeneklerimize aşağıdaki bağlantıdan ulaşabilirsin.
📄 Fiyat Listesi: https://bit.ly/Bonjukbay_FiyatListesi
🏠 Konaklama: https://bonjukbay.com/accommodation.html

BONJUK BAY BİLGİLENDİRME
Belirttiğin tarihlerde hangi etkinliğin yapılacağı henüz netleşmediği için şu anda etkinlik detaylarını ve ücret bilgisini veremiyorum. Ücret, etkinlik kesinleştiğinde ayrıca paylaşılacak, bilgin olsun.

{event_fee_info}

2026 Güncelleme: Bu sezon ritmimizi biraz daha gündüze taşıyoruz. Hafta içi 12:00, hafta sonu da 01:00'den sonra müzik olmayacak. Doğanın, dengenin ve anda kalmanın önceliklendiği; daha yumuşak, daha bilinçli ve daha sağlıklı bir Bonjuk deneyimine davetlisin. 🌀

Değerlendirmen sonrası bilgi verirsen süreci devam ettirmek isterim.

Sevgiler,
Bonjuk Bay Ekibi 🧿""",

        "confirm_payment": """Sevgili {first_name},

{check_in} - {check_out} tarihleri arasında 2 kişi için {room_type} konaklama ücretimiz açık büfeden servis edilen 3 öğün yemek dahil {total_price}'dur.

Rezervasyonunu onaylamak için aşağıdaki hesap bilgilerimize {deposit_amount} ödeme göndermeni ve dekontu bizimle paylaşmanı rica ederiz.

Kredi kartıyla ödemek istersen de aşağıdaki linki kullanabilirsin:
[ÖDEME LİNKİ]

Rezervasyonunu 24 saatliğine opsiyonluyoruz.

Hesap Adı: GRANT ZAFER TURİZM İNŞAAT MADEN SANAYİ VE TİCARET LİMİTED ŞİRKETİ
IBAN: TR490006701000000034479515
SWIFT Kodu (EUR, USD): YAPITRISXXX
SWIFT Kodu (Diğer Döviz Cinsleri): YAPITRISFEX
Açıklama: {guest_name} / {check_in}

2026 Güncelleme: Bu sezon ritmimizi biraz daha gündüze taşıyoruz. Hafta içi 12:00, hafta sonu da 01:00'den sonra müzik olmayacak. Doğanın, dengenin ve anda kalmanın önceliklendiği; daha yumuşak, daha bilinçli ve daha sağlıklı bir Bonjuk deneyimine davetlisin. 🌀

Değerlendirmen sonrası bilgi verirsen süreci devam ettirmek isterim.

Görüşmek dileğiyle 🎈""",

        "kids_week": """Sevgili {first_name},

Bu sene 26-30 Temmuz ve 16-20 Ağustos tarihlerinde Çocuk Haftası etkinliklerimizi düzenleyeceğiz. Bu tarihlerde çocukların kendi yaş grupları ile sosyalleşebilecekleri bir alan oluşturuyoruz.

Çocuk Haftası süresince çocukların sosyal becerilerini ve yaratıcılıklarını geliştirici yönde yaş gruplarına göre bedensel hareket, oyun ve sanatla dolu aktiviteler düzenliyoruz.

Fiyatlarımız tercih ettiğiniz konaklama seçeneklerine ve çocuklarınızın yaşlarına göre değişkenlik gösteriyor.
0-2 yaş çocuklar için ücret almıyoruz.
2-5 yaş arasına %50, 6-12 yaş için ise %20 konaklama indirimi uyguluyoruz.

Çocuk Haftası etkinliğimizde 2 yaşından büyük çocuklar için kişi başı nakit indirimli 100 euro etkinlik ücreti rica ediyoruz. Kredi kartı ya da havale yolunu tercih edersen 120 euro olarak dikkate almanı rica ederim.

Seneye Çocuk Haftası'nda görüşmek üzere 🎈""",

        "rejection_kids": """Sevgili {first_name},

Maalesef koyumuzda, etkinlik olmayan Pazartesi-Perşembe günleri arasında ve senede iki kez düzenlediğimiz Çocuk Haftası etkinliklerimiz dışında küçük misafirlerimizi ağırlayamıyoruz.

Anlayışın için teşekkür ederiz.""",

        "rejection_pets": """Sevgili {first_name},

Bonjuk Bay'de doğada birçok hayvanla birlikte yaşadığımız için içerideki atmosferi korumak adına üzülerek misafir hayvan dostlarımızı kabul edemiyoruz.

Anlayışın için teşekkür ederiz.""",

        "daily_use": """Merhaba,

Günlük kullanım ücretimiz açık büfeden servis edilen 1 öğün yemek dahil kişi başı 100 euro'dur. Müzik bitene kadar alanda vakit geçirebilirsiniz.

Günlük kullanım rezervasyonunuz için gelmeden 1 gün önce 05378102705 numaralı telefonumuzun Whatsapp'ına gelecek kişilerin ismini yazdırarak rezervasyon oluşturtabilirsiniz.

Sevgiler,""",

        "event_details": """Sevgili {first_name},

Eğer daha önce etkinliklerimize katıldıysan, Bonjuk Bay'in kendine özgü ruhunu ve ruh–zihin–beden bütünlüğünü gözeten akışını az çok hatırlıyorsundur.

Genel olarak etkinliklerimizde chi gong, yoga, nefes çalışmaları, sound healing, ritim atölyesi, sanat workshopları ve DJ performansları yer alıyor.

Bahsettiğin etkinlikler arasında ise sadece tema farkı bulunuyor. Akış genelde benzer oluyor; sadece eğitmenlerimiz ve sanatçılarımız değişiyor.

Temaya göre dress code'lar belirlenebiliyor ama kesinlikle zorunlu değil, tamamen keyfine kalmış.

Tüm bu detaylar da genellikle etkinlikten 1–2 hafta önce netleşiyor ve katılımcılarla o zaman paylaşılıyor.

Görüşmek dileğiyle,""",

        "minimum_stay": """Sevgili {first_name},

Koyumuzda alanlar ortak yaşam ve paylaşım prensibiyle kullanıldığı için, etkinlik sırasında yalnızca katılımcı misafirleri ağırlayabiliyoruz. Bu sebeple, etkinliğe katılım opsiyonel değil; konaklayan herkes etkinliğin bir parçası olarak kabul ediliyor.

Maalesef Bonjuk Burn, Dans Hafta Sonu ve Aşk Hafta Sonu birlikteliklerimizde, kendi konaklama seçeneklerimiz için minimum 4 gecelik rezervasyon alabiliyoruz.

2–3 gece katılmak isteyen misafirlerimize ise genellikle sadece own tent (kendi çadırıyla katılım) opsiyonu sunabiliyoruz.

Görüşmek dileğiyle,""",

        "reservation_cancelled": """Sevgili {first_name},

Uzun süredir senden bir dönüş alamadığımız için rezervasyonunu iptal etmek durumunda kaldık.

Eğer ileride aynı tarihler için ya da farklı bir dönem için tekrar rezervasyon yapmak istersen, her zaman bize ulaşabilirsin.

İlerleyen zamanlarda görüşmek dileğiyle 🎈""",

        "check_in_info": """Sevgili {first_name},

Ödeme ve bilgilendirme için teşekkürler 🙂

Check out saatimiz 11:00, check-in saatimiz 14:00'dır. Check-in saatinizden erken gelirseniz odanız/çadırınız hazırlanana kadar alanda vakit geçirebilirsiniz.

Bonjuk Bay'de yemek israfı olmamasına çok özen gösteriyoruz bu sebeple netleştiğinde bizimle geliş saatinizi ve herhangi bir gıda alerjiniz / beslenme tercihiniz varsa paylaşırsanız çok seviniriz.

Bonjuk Bay'e dışarıdan yiyecek ve/veya içecek (alkollü ya da alkolsüz) getirmemenizi önem ve özellikle rica ediyoruz.

Koyumuzda hizmet veren terapistlerimizden seans almanız halinde ödemesinin nakit yapılmasını rica ediyoruz, bu nedenle gelirken yanınızda nakit getirmenizi öneririz.

Görüşmek üzere. 🎈""",

        "airport_transfer": """Sevgili {first_name},

Havaalanı transfer talebiniz için lütfen gelişinizden en az 2 gün önce aşağıdaki formu doldurmanızı rica ederiz.
HAVALİMANI TRANSFER TALEP FORMU

Dalaman Havalimanı - Bonjuk Bay
1-3 kişi taksi: 3100 TL
1-7 kişi van: 3400 TL
1-13 kişi sprinter: 4200 TL

Organize oluyoruz. Üzerinde adınız yazılı bir pankartla terminal çıkışında karşılanacaksınız.

Görüşmek üzere. 🎈"""
    },

    "en": {
        "welcome": """Dear {first_name},

Thank you for your interest in Bonjuk Bay; we would love to welcome you among us.

You can access our 2026 price list and accommodation options for your reference from the links below:
📄 Price List: https://bit.ly/Bonjukbay_FiyatListesi
🏠 Accommodation: https://bonjukbay.com/accommodation.html

BONJUK BAY INFORMATION
As the event scheduled for the mentioned dates has not yet been confirmed, I'm currently unable to provide detailed information or pricing. The event fee will be communicated once the schedule is finalized.

{event_fee_info}

2026 Update: This season, we're shifting our rhythm into the daylight. There will be no music after 1:00 AM on the weekends and 12:00 AM on the weekdays. We're inviting you into a softer, more conscious, and healthier Bonjuk experience—where nature, balance, and presence come first. See you in the vortex! 🌀

Please let us know your thoughts so we can proceed.

Best regards,
Bonjuk Bay Team 🧿""",

        "confirm_payment": """Dear {first_name},

Our accommodation price for 2 people from {check_in} to {check_out} for {room_type}, including three meals served from the open buffet, is {total_price}.

To confirm your reservation, we kindly ask you to send a {deposit_amount} deposit to the account details below and share the receipt with us.

If you prefer to pay by credit card, you can use the link below:
[PAYMENT LINK]

We are holding your reservation as an option for 24 hours.

Euro account:
Account Name: GRANT ZAFER TURİZM İNŞAAT MADEN SANAYİ VE TİCARET LİMİTED ŞİRKETİ
IBAN: TR490006701000000034479515
SWIFT Code (EUR, USD): YAPITRISXXX
SWIFT Code (other currencies): YAPITRISFEX
Transfer Note: {guest_name} / {check_in}

2026 Update: This season, we're shifting our rhythm into the daylight. There will be no music after 1:00 AM on the weekends and 12:00 AM on the weekdays. We're inviting you into a softer, more conscious, and healthier Bonjuk experience—where nature, balance, and presence come first. See you in the vortex! 🌀

Please let us know your thoughts so we can proceed.

See you soon! 🎈""",

        "rejection_kids": """Dear {first_name},

Due to our property policy, we are only able to accommodate guests who are 18 years of age or older, except during our Kids Week events.

Thank you for your understanding.""",

        "rejection_pets": """Dear {first_name},

As Bonjuk Bay is home to many animals living freely in nature, we kindly ask for your understanding that we are not able to host guest pets on the property. This is to help preserve the delicate harmony of our natural environment.

Thank you for your love and respect for all beings who call this place home. 💛""",

        "check_in_info": """Dear {first_name},

Thank you for the payment and information 🙂

Our check-out time is 11:00, and check-in time is 14:00. If you arrive earlier than the check-in time, you can spend time in the area until your room/tent is prepared.

At Bonjuk Bay, we are very careful about not wasting food, so we would appreciate it if you could share your arrival time and any food allergies/dietary preferences once they are finalized.

We kindly and especially ask you not to bring any food or drinks (alcoholic or non-alcoholic) from outside to Bonjuk Bay.

If you are going to book a private session with our healers and therapists, we kindly request that payment be made in cash. Therefore, we recommend bringing cash with you.

See you soon. 🎈""",

        "airport_transfer": """Dear {first_name},

For your airport transfer request, please fill out the form below at least 2 days before your arrival date.
AIRPORT TRANSPORTATION REQUEST FORM

Dalaman Airport to Bonjuk Bay
1-3 px taxi: 3100 TL
1-7 px van: 3400 TL
1-13 px sprinter: 4200 TL

We are organizing everything. You will be greeted at the terminal exit with a sign bearing your name.

See you soon. 🎈""",

        "kids_week": """Dear {first_name},

This year, we will be hosting our Kids Week events on July 26-30 and August 16-20. During these dates, we create a space where children can socialize with their own age groups.

During Kids Week, we organize activities filled with physical movement, games, and art according to age groups to develop children's social skills and creativity.

Our prices vary depending on your preferred accommodation options and the ages of your children.
We do not charge for children aged 0-2.
We apply a 50% discount for ages 2-5 and a 20% accommodation discount for ages 6-12.

For our Kids Week event, we kindly request a participation fee of 100 euros per person (cash discount) for children over 2 years old. If you prefer to pay by credit card or bank transfer, please consider it as 120 euros.

See you at Kids Week next year! 🎈""",

        "daily_use": """Hello,

Our daily use fee is 100 euros per person, including 1 meal served from the open buffet. You can spend time in the area until the music ends.

For your daily use reservation, you can create a reservation by writing the names of the people who will come to our phone number 05378102705 on WhatsApp 1 day before coming.

Best regards,""",

        "event_details": """Dear {first_name},

If you've attended our events before, you probably remember Bonjuk Bay's unique spirit and flow that honors mind-body-spirit integration.

Generally, our events include chi gong, yoga, breathwork, sound healing, rhythm workshops, art workshops, and DJ performances.

The events you mentioned differ only in theme. The flow is generally similar; only our instructors and artists change.

Dress codes may be determined according to the theme, but they are definitely not mandatory—it's completely up to you.

All these details are usually finalized 1-2 weeks before the event and shared with participants at that time.

Looking forward to seeing you,""",

        "minimum_stay": """Dear {first_name},

Since the areas in our bay are used with the principle of communal living and sharing, we can only host participating guests during the event. Therefore, participation in the event is not optional; everyone staying is considered part of the event.

Unfortunately, for our Bonjuk Burn, Dance Weekend, and Love Weekend gatherings, we can only accept reservations for a minimum of 4 nights for our own accommodation options.

For guests who wish to participate for 2-3 nights, we can usually only offer the own tent (participation with your own tent) option.

Looking forward to seeing you,""",

        "reservation_cancelled": """Dear {first_name},

Since we have not received a response from you for a long time, we had to cancel your reservation.

If you would like to make a reservation again for the same dates or a different period in the future, you can always contact us.

Looking forward to connecting in the future 🎈"""
    }
}
