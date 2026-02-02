
import streamlit as st
import pandas as pd
import logging
import urllib.parse
from datetime import datetime
import sys
import os

# Streamlit Cloud için path ayarı (src klasörünü python path'e ekle)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.modules.reservation import validate_reservation
from src.modules.transfers import determine_vehicle_type, get_transfer_price_estimate, generate_supplier_order
from src.modules.email_hook import email_hook
from src.modules.ai_parser import ai_parser
from src.config import config

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

# Session State Başlatma (Eğer yoksa)
if 'temp_res_data' not in st.session_state:
    st.session_state['temp_res_data'] = ""
if 'mail_transfer_success' not in st.session_state:
    st.session_state['mail_transfer_success'] = False

@st.cache_data(ttl=300)  # 5 dakika önbellek
def get_unread_email_count():
    """Gmail'deki okunmamış mail sayısını cache'leyerek hızlı döndürür"""
    try:
        if email_hook.enabled:
            emails = email_hook.fetch_unseen_emails(limit=50)
            return len(emails)
    except:
        pass
    return 0

def show_dashboard():
    st.title("🧿 Bonjuk Ops Dashboard")
    st.subheader(f"Bugün: {datetime.now().strftime('%d/%m/%Y')}")
    
    # Cache'lenmiş mail sayısı
    unread_count = get_unread_email_count()
    
    # Session state'den rezervasyon sayısı
    parsed_count = 1 if 'parsed_res' in st.session_state and st.session_state['parsed_res'] else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Gelen Talepler", f"{parsed_count} Aktif", "+ Mail Hook" if email_hook.enabled else "⚠️ Devre Dışı")
    col2.metric("Okunmamış Mailler", f"{unread_count} Mail", "+ AI Parser" if ai_parser.enabled else "⚠️ Devre Dışı")
    col3.metric("Transfer Talebi", "Sistem Hazır", "🧿")


    st.divider()

    # Email Hook / Simülasyon Kısmı
    st.subheader("📬 Gelen Rezervasyon E-postaları")
    
    col_sim1, col_sim2 = st.columns(2)
    
    # Simülasyon Butonu
    if col_sim1.button("Simülasyon Modu (Alper Yılmaz .eml)", key="sim_mode_btn"):
        st.session_state['show_simulation'] = True
    
    if st.session_state.get('show_simulation'):
        sample = email_hook.get_sample_email()
        with st.expander(f"✉️ [SİMÜLASYON] {sample['subject']} ({sample['from']})", expanded=True):
            st.write(f"**Tarih:** {sample['date']}")
            st.text_area("İçerik:", sample['body'], height=150, key="sim_text_display", disabled=True)
            if st.button("Simüle Edilen Talebi Aktar (Test)", key="transfer_sim_btn"):
                st.session_state['temp_res_data'] = sample['body']
                st.session_state['show_simulation'] = False 
                st.session_state['mail_transfer_success'] = True
                st.rerun()

    # Gerçek Email Butonu
    if col_sim2.button("Gerçek E-postaları Tara", key="real_email_btn"):
        if email_hook.enabled:
            with st.spinner("Gelen kutuna bakıyorum..."):
                recent_emails = email_hook.fetch_unseen_emails()
                if recent_emails:
                    st.session_state['fetched_emails'] = recent_emails # Cache results temporarily
                else:
                    st.session_state['fetched_emails'] = []
                    st.success("Harika! Okunmamış rezervasyon maili yok. 🧿")
        else:
             st.warning("⚠️ E-posta bağlantısı kurulu değil. Lütfen .env dosyasını kontrol edin.")

    # E-mailleri Listele (Varsa)
    if 'fetched_emails' in st.session_state and st.session_state['fetched_emails']:
        for em in st.session_state['fetched_emails']:
            with st.expander(f"✉️ {em['subject']} ({em['from']})"):
                st.write(f"**Tarih:** {em['date']}")
                st.text_area("İçerik:", em['body'][:500] + "...", height=150, key=f"text_{em['id']}")
                
                # Transfer Butonu
                if st.button(f"Talebi Uygulamaya Aktar", key=f"btn_{em['id']}"):
                    st.session_state['temp_res_data'] = em['body']
                    st.session_state['mail_transfer_success'] = True
                    # E-posta listesini temizle ki kafa karışmasın
                    del st.session_state['fetched_emails']
                    st.rerun()

    # Başarı Mesajı (Yeniden Yönlendirme Uyarısı)
    if st.session_state.get('mail_transfer_success'):
        st.success("✅ Veri başarıyla yakalandı! Lütfen soldaki menüden '📅 Rezervasyon Talebi' sekmesine geçin.")
        # Kullanıcı mesajı gördükten sonra bu flag'i kaldırabiliriz
        # Ama şimdilik kalsın, rezervasyon sayfasına geçince silinir.

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
                    st.session_state['form_special_requests'] = parsed_data.get('special_requests', "")

                    st.success("Veriler başarıyla ayıklandı! 👇 Aşağıdaki formu kontrol edip '✅ Bilgileri Onayla' butonuna basın.")
                else:
                    st.error("AI veriyi okuyamadı. (Detay: API yanıt vermedi veya format hatalı)")

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
        
        special_requests = st.text_area("📝 Özel İstekler / Notlar", value=p.get('special_requests', ""), height=100, key="form_special_requests", 
                                        help="Doğum günü pastası, erken check-in, özel yemek tercihleri vb.")
        
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
            st.text_area("Hazırlanan Yanıt:", value=st.session_state['ai_reply'], height=300, key="final_ai_reply_v2")
            
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
    
    # Onaylanmış rezervasyon verisini al (varsa)
    res_data = st.session_state.get('approved_data', {})
    parsed_res = st.session_state.get('parsed_res', {})
    
    # Verileri hazırla (önce approved_data, yoksa parsed_res, yoksa placeholder)
    guest_name = res_data.get('guest_name') or parsed_res.get('guest_name', '[Misafir Adı]')
    first_name = guest_name.split()[0].title() if guest_name and guest_name != '[Misafir Adı]' else '[Ad]'
    check_in = res_data.get('check_in') or parsed_res.get('check_in', '[Giriş Tarihi]')
    check_out = res_data.get('check_out') or parsed_res.get('check_out', '[Çıkış Tarihi]')
    room_type = res_data.get('room_type') or parsed_res.get('accommodation_type', '[Oda Tipi]')
    pax = res_data.get('pax') or parsed_res.get('pax', '[Kişi Sayısı]')
    nationality = parsed_res.get('nationality', 'Foreign')
    missing_info = res_data.get('missing_info') or parsed_res.get('missing_info', [])
    missing_info_str = ', '.join(missing_info) if isinstance(missing_info, list) and missing_info else '[Eksik Bilgi]'

    # Otomatik dil seçimi: Türk ise TR, değilse EN
    auto_lang_index = 0 if nationality == 'Turkish' else 1
    lang_options = ["Türkçe 🇹🇷", "English 🇺🇸"]
    
    # Dil seçimi (otomatik önerilir ama kullanıcı değiştirebilir)
    lang_tab = st.radio("Dil Seçimi / Language Selection", lang_options, index=auto_lang_index, horizontal=True)
    
    if res_data or parsed_res:
        st.success(f"📌 Aktif Rezervasyon: **{guest_name}** | {check_in} → {check_out} | {pax} Kişi | {room_type}")

    if lang_tab == "Türkçe 🇹🇷":
        templates = {
            "🆕 Yeni Talep Karşılama": f"""Sevgili {first_name},

Rezervasyon talebiniz bize ulaştı. En kısa sürede sizinle iletişime geçeceğiz.

**Rezervasyon Detayları:**
- Misafir Adı: {guest_name}
- Oda Tipi: {room_type}
- Giriş: {check_in}
- Çıkış: {check_out}
- Kişi Sayısı: {pax}

Teşekkürler,
Bonjuk Bay Team 🧿""",
            "❓ Eksik Bilgi Talebi": f"""Sevgili {first_name},

Rezervasyon talebin harika görünüyor. Seni aramızda görmeyi çok isteriz.

Size en uygun yerleşimi yapabilmemiz için ufak bir detaya ihtiyacımız var:
👉 **{missing_info_str}**

Bu bilgiyi bizimle paylaşırsan işlemlere hemen devam edebiliriz.

Warm hugs! ✨""",
            "✅ Konfirmasyon & Ödeme": f"""Sevgili {first_name},

Bonjuk Bay'e ilgine teşekkür ederiz, sizi aramızda görmeyi çok isteriz.

Referans olması için 2026 fiyat listemize ve konaklama seçeneklerimize aşağıdaki bağlantılardan ulaşabilirsin:

📄 Fiyat Listesi: https://bit.ly/Bonjukbay_FiyatListesi
🏠 Konaklama: https://bonjukbay.com/accommodation.html

{check_in} - {check_out} tarihleri arasındaki rezervasyonunu {room_type} için opsiyonladık.

Rezervasyonunu onaylamak için aşağıdaki hesap bilgilerimize ödeme göndermeni ve dekontu bizimle paylaşmanı rica ederiz.

Rezervasyonunu 24 saatliğine opsiyonluyoruz.

🏦 Hesap Adı: GRANT ZAFER TURİZM İNŞAAT MADEN SANAYİ VE TİCARET LİMİTED ŞİRKETİ
IBAN: TR490006701000000034479515
SWIFT (EUR/USD): YAPITRISXXX
Açıklama: {guest_name} / {check_in}

Warm hugs! 🧿""",
            "🚫 Müsaitlik Yok": f"""Sevgili {first_name},

Tarihlerini kontrol ettik fakat maalesef belirtilen tarihlerde ({check_in} - {check_out}) {room_type} için doluyuz. 😔

Ancak seninle alternatif tarihleri veya oda seçeneklerini konuşmak isteriz.

Haberleşelim, senin için en güzelini ayarlayalım! 🧿
Warm hugs!""",
            "⏳ Ödeme Hatırlatma": f"""Sevgili {first_name},

Selamlar! Rezervasyon opsiyonunun süresi dolmak üzere.
Yerini tutmaya devam etmek istiyoruz ama sistemi açmamız gerekebilir.

Eğer hala gelmeyi planlıyorsan, lütfen bugün içinde dekontu bizimle paylaş.
Bir aksilik varsa da haber ver, yardımcı olalım.

Sevgiler,
Bonjuk Bay Team 🧿"""
        }
    else:
        templates = {
            "🆕 New Request Welcome": f"""Dear {first_name},

Your reservation request has reached us. We will contact you as soon as possible.

**Reservation Details:**
- Guest Name: {guest_name}
- Room Type: {room_type}
- Check-In: {check_in}
- Check-Out: {check_out}
- Pax: {pax}

Thank you,
Bonjuk Bay Team 🧿""",
            "❓ Missing Information": f"""Hi {first_name},

We are excited about your request! 🧿 However, we need one more little piece of information to prepare the best offer for you:

**Missing Information:** {missing_info_str}

Once you share this with us, we will send your offer immediately.

Warm hugs! ✨""",
            "✅ Confirmation & Payment": f"""Hi {first_name},

Thank you for your interest in Bonjuk Bay! We can't wait to see you with us.

📄 Price List: https://bit.ly/Bonjukbay_FiyatListesi
🏠 Accommodation: https://bonjukbay.com/accommodation.html

We have optioned your reservation for {room_type} between {check_in} - {check_out} for 24 hours.

🏦 Bank Details:
Account Name: GRANT ZAFER TURİZM İNŞAAT MADEN SANAYİ VE TİCARET LİMİTED ŞİRKETİ
IBAN: TR490006701000000034479515
SWIFT (EUR/USD): YAPITRISXXX
Reference: {guest_name} / {check_in}

Warm hugs! 🧿""",
            "🚫 Not Available": f"""Dear {first_name},

We checked the dates but unfortunately {room_type} is fully booked for {check_in} - {check_out}. 😔

However, we would love to discuss alternative dates or room options with you.

Let's find the best solution for you! 🧿
Warm hugs!""",
            "⏳ Payment Reminder": f"""Dear {first_name},

Just a friendly reminder that your reservation option is about to expire.
We want to keep your spot, but we may need to release it soon.

If you're still planning to come, please share the payment receipt with us today.

Best regards,
Bonjuk Bay Team 🧿"""
        }

    for title, content in templates.items():
        with st.expander(title):
            # Key'in sonuna _v2 ekledik ki cache temizlensin, yeni linkler görünsün
            st.text_area("Yanıt Metni:", value=content, height=200, key=f"tpl_{title}_v2")

