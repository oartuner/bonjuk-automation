import streamlit as st
import pandas as pd
import logging
import urllib.parse
from datetime import datetime
from modules.reservation import validate_reservation
from modules.transfers import determine_vehicle_type, get_transfer_price_estimate, generate_supplier_order
from modules.email_hook import email_hook
from modules.ai_parser import ai_parser

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BonjukOps")

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Bonjuk Bay Operasyon Merkezi",
    page_icon="🧿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Stil Uygulama
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #1f77b4; color: white; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🧿 Bonjuk Ops")
menu = st.sidebar.radio("Menü", ["🏠 Ana Sayfa", "📅 Rezervasyon Talebi", "🚗 Transfer Planlayıcı", "📜 Hazır Yanıtlar"])

def show_dashboard():
    st.title("🧿 Bonjuk Ops Dashboard")
    st.subheader(f"Bugün: {datetime.now().strftime('%d/%m/%Y')}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Gelen Talepler", "Aktif", "Mail Hook")
    col2.metric("Okunmamış Mailler", "Check", "AI Parser")
    col3.metric("Transfer Talebi", "Sistem Hazır", "🧿")

    st.divider()

    # Email Hook / Simülasyon Kısmı
    st.subheader("📬 Gelen Rezervasyon E-postaları")
    
    col_sim1, col_sim2 = st.columns(2)
    
    if col_sim1.button("Simülasyon Modu (Alper Yılmaz .eml)", key="sim_mode_btn"):
        st.session_state['show_simulation'] = True
    
    if st.session_state.get('show_simulation'):
        sample = email_hook.get_sample_email()
        with st.expander(f"✉️ [SİMÜLASYON] {sample['subject']} ({sample['from']})", expanded=True):
            st.write(f"**Tarih:** {sample['date']}")
            st.text_area("İçerik:", sample['body'], height=150, key="sim_text_display", disabled=True)
            if st.button("Simüle Edilen Talebi Aktar (Test)", key="transfer_sim_btn"):
                st.session_state['temp_res_data'] = sample['body']
                st.session_state['show_simulation'] = False # İşlem bitince kapat
                st.success("Simülasyon verisi yakalandı! Şimdi 'Rezervasyon Talebi' sekmesine geçin. 🧿")

    if col_sim2.button("Gerçek E-postaları Tara", key="real_email_btn"):
        if email_hook.enabled:
            with st.spinner("Gelen kutuna bakıyorum..."):
                recent_emails = email_hook.fetch_unseen_emails()
                if recent_emails:
                    for em in recent_emails:
                        with st.expander(f"✉️ {em['subject']} ({em['from']})"):
                            st.write(f"**Tarih:** {em['date']}")
                            st.text_area("İçerik:", em['body'][:500] + "...", height=150, key=f"text_{em['id']}")
                            if st.button(f"Talebi Uygulamaya Aktar", key=f"btn_{em['id']}"):
                                st.session_state['temp_res_data'] = em['body']
                                st.success("Veri yakalandı! 'Rezervasyon Talebi' sekmesinde AI ile işleyebilirsiniz. 🧿")
                else:
                    st.success("Harika! Okunmamış rezervasyon maili yok. 🧿")
    else:
        st.warning("⚠️ E-posta bağlantısı kurulu değil. Lütfen .env dosyasını kontrol edin.")

    st.divider()
    st.info("💡 Not: Supabase entegrasyonu devre dışı bırakıldı. Veriler yerel olarak AI ile işlenmektedir.")

if menu == "🏠 Ana Sayfa":
    show_dashboard()

elif menu == "📅 Rezervasyon Talebi":
    st.header("🪄 Akıllı Rezervasyon Girişi")
    
    initial_text = st.session_state.get('temp_res_data', "")
    raw_text = st.text_area("Rezervasyon Metni (E-posta veya Mesaj):", value=initial_text, height=200, help="Buraya mail içeriğini yapıştırın.")
    
    if st.button("🪄 AI ile Bilgileri Ayıkla (Gemini)"):
        if not ai_parser.enabled:
            st.error("AI API anahtarı eksik! Lütfen .env dosyasına GEMINI_API_KEY ekleyin.")
        elif not raw_text:
            st.warning("Lütfen işlem yapılacak bir metin girin.")
        else:
            with st.spinner("AI verileri ayıklıyor..."):
                parsed_data = ai_parser.parse_reservation(raw_text)
                if parsed_data:
                    st.session_state['parsed_res'] = parsed_data
                    
                    # Form widget'larını manuel olarak güncelle (Streamlit state yönetimi için)
                    st.session_state['form_guest_name'] = parsed_data.get('guest_name', "")
                    st.session_state['form_check_in'] = parsed_data.get('check_in', "")
                    st.session_state['form_check_out'] = parsed_data.get('check_out', "")
                    if parsed_data.get('pax'):
                        st.session_state['form_pax'] = int(parsed_data['pax'])
                    st.session_state['form_lang'] = parsed_data.get('guest_language', "tr")
                    st.session_state['form_nationality'] = parsed_data.get('nationality', "")
                    st.session_state['form_room_type'] = parsed_data.get('accommodation_type', "Sea View Room")

                    st.success("Veriler başarıyla ayıklandı! 👇 Aşağıdaki formu kontrol edip '✅ Bilgileri Onayla' butonuna basın.")
                else:
                    st.error("AI veriyi okurken bir sorun yaşadı.")

    st.divider()

    p = st.session_state.get('parsed_res', {})
    
    with st.form("res_form"):
        guest_name = st.text_input("Misafir Adı", value=p.get('guest_name', ""), key="form_guest_name")
        col_lang, col_nat = st.columns(2)
        guest_lang = col_lang.selectbox("Yazışma Dili", ["tr", "en"], index=0 if p.get('guest_language') == 'tr' else 1, key="form_lang")
        nationality = col_nat.text_input("Milliyet (Passport/ID Kaynaklı)", value=p.get('nationality', ""), key="form_nationality")

        col1, col2 = st.columns(2)
        check_in = col1.text_input("Giriş Tarihi (YYYY-MM-DD)", value=p.get('check_in', ""), key="form_check_in")
        check_out = col2.text_input("Çıkış Tarihi (YYYY-MM-DD)", value=p.get('check_out', ""), key="form_check_out")
        
        pax = st.number_input("Kişi Sayısı (Pax)", min_value=1, value=int(p.get('pax', 1)) if isinstance(p.get('pax'), int) else 1, key="form_pax")
        room_type = st.selectbox("Oda Tipi", ["Sea View Room", "Sea Front Room", "Lotus Bell Tent", "Safari Tent", "Kendi Çadırı"], index=0, key="form_room_type")
        
        notes = st.text_area("Özel Notlar (Alerji, Kutlama vb.)", key="form_notes")
        
        submitted = st.form_submit_button("✅ Bilgileri Onayla")
        
        if submitted:
            st.success(f"📌 {guest_name} için veriler doğrulandı!")
            st.session_state['approved_data'] = {
                "guest_name": guest_name,
                "pax": pax,
                "check_in": check_in,
                "check_out": check_out,
                "room_type": room_type,
                "guest_language": guest_lang,
                "missing_info": p.get('missing_info', [])
            }

    if st.session_state.get('approved_data'):
        st.divider()
        st.subheader("📩 Akıllı Yanıt Asistanı")
        
        resp_col1, resp_col2 = st.columns(2)
        lang_suffix = " Taslağı Üret" if st.session_state['approved_data']['guest_language'] == 'tr' else " Draft"
        
        if resp_col1.button(f"✉️ Eksik Bilgi{lang_suffix}"):
            with st.spinner("Hazırlanıyor..."):
                reply = ai_parser.generate_response(st.session_state['approved_data'], "Eksik Bilgi" if st.session_state['approved_data']['guest_language'] == 'tr' else "Missing Information")
                st.session_state['ai_reply'] = reply

        if resp_col2.button(f"✅ Konfirmasyon{lang_suffix}"):
            with st.spinner("Hazırlanıyor..."):
                reply = ai_parser.generate_response(st.session_state['approved_data'], "Konfirmasyon" if st.session_state['approved_data']['guest_language'] == 'tr' else "Confirmation")
                st.session_state['ai_reply'] = reply

        if st.session_state.get('ai_reply'):
            st.text_area("Hazırlanan Yanıt:", value=st.session_state['ai_reply'], height=300, key="final_ai_reply")
            
            # WhatsApp & Email Redirects
            encoded_text = urllib.parse.quote(st.session_state['ai_reply'])
            wa_link = f"https://wa.me/?text={encoded_text}"
            
            # Mailto Link
            mail_subject = urllib.parse.quote(f"Bonjuk Bay Reservation - {st.session_state['approved_data']['guest_name']}")
            mail_link = f"mailto:?subject={mail_subject}&body={encoded_text}"
            
            btn_col1, btn_col2 = st.columns(2)
            
            with btn_col1:
                st.markdown(f"""
                    <a href="{wa_link}" target="_blank" style="text-decoration:none; display:block;">
                        <div style="width:100%; padding:10px; background-color:#25D366; color:white; border:none; border-radius:5px; cursor:pointer; font-weight:bold; text-align:center;">
                            📱 WhatsApp'a Aktar
                        </div>
                    </a>
                """, unsafe_allow_html=True)
            
            with btn_col2:
                st.markdown(f"""
                    <a href="{mail_link}" target="_blank" style="text-decoration:none; display:block;">
                        <div style="width:100%; padding:10px; background-color:#1f77b4; color:white; border:none; border-radius:5px; cursor:pointer; font-weight:bold; text-align:center;">
                            📧 E-posta Taslağı Aç
                        </div>
                    </a>
                """, unsafe_allow_html=True)
                
            st.info("💡 Yukarıdaki butonlar metni otomatik olarak ilgili uygulamaya taşır.")

elif menu == "🚗 Transfer Planlayıcı":
    st.header("Araç ve Fiyat Planlayıcı")
    pax = st.number_input("Yolcu Sayısı", min_value=1, value=1, key="transfer_pax_input")
    route = st.selectbox("Güzergah", ["Dalaman-Bonjuk", "Bodrum-Bonjuk"], key="transfer_route_select")
    
    vehicle = determine_vehicle_type(pax)
    estimate = get_transfer_price_estimate(route, pax)
    
    st.metric("Önerilen Araç", vehicle)
    st.metric("Tahmini Maliyet", f"{estimate} TL")
    
    if st.button("Tedarikçi İş Emri Hazırla"):
        order = generate_supplier_order("Misafir", route, "Belirtilmedi", pax, "Belirtilmedi")
        st.text_area("İş Emri Metni:", value=order, height=250)

elif menu == "📜 Hazır Yanıtlar":
    st.header("📖 Bonjuk Bay Ortak Yanıt Kütüphanesi")
    lang_tab = st.radio("Dil Seçimi / Language Selection", ["Türkçe 🇹🇷", "English 🇺🇸"], horizontal=True)

    if lang_tab == "Türkçe 🇹🇷":
        templates = {
            "🆕 Yeni Talep Karşılama": """Dear [Misafir Adı],

Rezervasyon talebiniz bize ulaştı. En kısa sürede sizinle iletişime geçeceğiz.

**Rezervasyon Detayları:**
- Guest Name: [Ad Soyad]
- Room Type: [Oda Tipi]
- Check-In: [Tarih]
- Check-Out: [Tarih]
- Pax: [Sayı]

Teşekkürler,
Bonjuk Bay Team 🧿""",
            "❓ Eksik Bilgi Talebi": """Sevgili [Ad],

Rezervasyon talebin harika görünüyor. Seni aramızda görmeyi çok isteriz.

Size en uygun yerleşimi yapabilmemiz için ufak bir detaya ihtiyacımız var:
👉 **[Eksik Alan Giriniz]**

Bu bilgiyi bizimle paylaşırsan işlemlere hemen devam edebiliriz.

Warm hugs! ✨""",
            "✅ Konfirmasyon & Ödeme": """Sevgili [Ad],

Bonjuk Bay'e ilgine teşekkür ederiz, sizi aramızda görmeyi çok isteriz.

Referans olması için 2026 fiyat listemize ve konaklama seçeneklerimize aşağıdaki bağlantılardan ulaşabilirsin:

2026 Fiyat Listesi:
https://bonjukbay-my.sharepoint.com/personal/reservation_bonjukbay_com/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Freservation%5Fbonjukbay%5Fcom%2FDocuments%2FBerk%20Lenovo%20Desktop%2FBonjuk%20Bay%2025%20%2D%20Price%20List%2Epdf&parent=%2Fpersonal%2Freservation%5Fbonjukbay%5Fcom%2FDocuments%2FBerk%20Lenovo%20Desktop&ga=1

Konaklama Seçenekleri:
https://bonjukbay.com/accommodation.html

[Giriş] - [Çıkış] tarihleri arasındaki rezervasyonunu [Oda Tipi] için opsiyonladık.
Konaklama ücretimiz [Tutar] olup, erken rezervasyon indirimi vb. uygulanmıştır.

Rezervasyonunu onaylamak için aşağıdaki hesap bilgilerimize ödeme göndermeni ve dekontu bizimle paylaşmanı rica ederiz.

Kredi kartıyla ödemek istersen de aşağıdaki linki kullanabilirsin:
[ÖDEME LINKI]

Rezervasyonunu 24 saatliğine opsiyonluyoruz.

Hesap Adı : GRANT ZAFER TURİZM İNŞAAT MADEN SANAYİ VE TİCARET LİMİTED ŞİRKETİ
IBAN : TR490006701000000034479515
SWIFT Kodu (EUR, USD) : YAPITRISXXX
SWIFT Kodu (Diğer Döviz Cinsleri) : YAPITRISFEX
Açıklama: [Misafir Adı] / [Giriş Tarihi]

2026 Update: Bu sezon ritmimizi biraz daha gündüze taşıyoruz. Hafta sonu 01:00’den sonra müzik olmayacak. Doğanın, dengenin ve anda kalmanın önceliklendiği; daha yumuşak, daha bilinçli ve daha sağlıklı bir Bonjuk deneyimine davetlisin!

Warm hugs!""",
            "🚫 Müsaitlik Yok (Alternatif Öneri)": """Sevgili [Ad],

Tarihlerini kontrol ettik fakat maalesef belirtilen tarihlerde [Oda Tipi] için doluyuz. 😔

Ancak şu tarihlerde sana harika bir yer açabiliriz:
🗓️ **[Alternatif Tarihler]**

Ya da istersen aynı tarihlerde **[Alternatif Oda]** seçeneğimiz müsait.

Haberleşelim, senin için en güzelini ayarlayalım! 🧿
Warm hugs!""",
            "👥 Grup Rezervasyonu (Event Sorusu)": """Sevgili [Ad],

Kalabalık gelmeniz harika olur! Bonjuk toplu enerjiyi çok sever. 🧿
Grup rezervasyonlarında süreci daha rahat yönetebilmek için bazı detaylara ihtiyacımız var:

- Tam kişi sayısı
- Kadın/Erkek dağılımı (Oda yerleşimi için)
- Özel bir kutlama/event planınız var mı?

Bu detayları paylaşırsan size özel bir plan çıkaralım.
Warm hugs! ✨""",
            "⏳ Ödeme Hatırlatma": """Sevgili [Ad],

Selamlar! Rezervasyon opsiyonunun süresi dolmak üzere.
Yerini tutmaya devam etmek istiyoruz ama sistemi açmamız gerekebilir.

Eğer hala gelmeyi planlıyorsan, lütfen bugün içinde dekontu veya ödeme bilgisini bizimle paylaş.
Bir aksilik varsa da haber ver, yardımcı olalım.

Sevgiler,
Bonjuk Bay Team 🧿"""
        }
    else:
        templates = {
            "🆕 New Request Welcome": """Dear [Guest Name],

Your reservation request has reached us. We will contact you as soon as possible.

**Reservation Details:**
- Guest Name: [Full Name]
- Room Type: [Room Type]
- Check-In: [Date]
- Check-Out: [Date]
- Pax: [Count]

Thank you for choice... 
Bonjuk Bay Team 🧿""",
            "❓ Missing Information": """Hi [Guest Name],

We are excited about your request! 🧿 However, we need one more little piece of information to prepare the best offer for you:
 
**Missing Information:** [Field Name]

Once you share this with us, we will send your offer immediately.

Warm hugs! 🕯️✨""",
            "✅ Confirmation & Payment": """Hi [Guest Name],

We can't wait to see you with us! 🧿 We have optioned your reservation for 24 hours. To complete your registration, please follow the payment details.

**Summary Details:**
- Dates: [Check-In] - [Check-Out]
- Room: [Room Type]
- Amount: [Amount]

See you soon! 🌞
Warm hugs!"""
        }

    for title, content in templates.items():
        with st.expander(title):
            st.text_area("Yanıt Metni:", value=content, height=150, key=f"tpl_{title}")
