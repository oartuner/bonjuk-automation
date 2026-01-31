# 🧿 Bonjuk Bay Operasyonel El Kitabı (Operational Manual)

> Bu belge, Bonjuk Bay'in günlük operasyonel akışlarını (Rezervasyon, Transfer, Misafir İletişimi) standartlaştırmak ve otomatize etmek amacıyla hazırlanmıştır. Abine/Ekibe doğrudan iletmek için uygundur.

---

## 🛠 Kullanılan Araçlar (Tech Stack)
*   **Elektra (PMS):** Rezervasyon, Check-in/out, Folio işlemleri.
*   **PowerApps:** Operasyonel formlar (Check-in, Transfer talepleri).
*   **Power Automate / n8n:** Otomasyon beyni (Tetikleyiciler, E-postalar).
*   **İletişim:** WhatsApp, Instagram (DM), E-posta (`reservation@bonjukbay.com`).
*   **Takip:** Google Sheets / Excel (Lead ve operasyon logları).

---

## 📋 Operasyonel Akışlar (Workflows)

### A) Rezervasyon Talebi Alımı ve İlk Yanıt
**Amaç:** Gelen talebi karşılamak, eksik bilgiyi tamamlamak ve misafire "Seninle ilgileniyoruz" hissi vermek.

*   **Tetikleyici (Trigger):**
    *   App üzerindeki Dropdown Form -> `reservation@` adresine düşen e-posta.
    *   Doğrudan E-posta, Instagram DM veya WhatsApp mesajı.
*   **Gerekli Bilgiler (Input):**
    *   Ad Soyad
    *   Tarihler (Giriş - Çıkış)
    *   Kişi Sayısı (Pax)
    *   Konaklama Tipi (Oda, Çadır, Kendi Çadırı vb.)
    *   Özel Notlar (Diyet, Alerji, Kutlama)
*   **Operasyon Kuralı:**
    *   Bilgi eksikse: Tek seferde tüm eksikleri soran nazik bir mesaj at.
    *   Tarih doluysa: Alternatif tarih/oda öner.
    *   **Kritik:** İletişim hangi kanaldan (IG, WA) gelirse gelsin, ana kayıt kaynağı **E-posta Thread'i** olsun.
*   **Çıktı:**
    *   Misafire: "Talebinizi aldık" + Eksik bilgi sorusu.
    *   İç Ekip: Lead listesine (Spreadsheet) kayıt.

---

### B) Uygunluk & Fiyat Teklifi Hazırlama (Quote)
**Amaç:** Misafire net, anlaşılır ve tek sayfada bir teklif sunmak.

*   **Tetikleyici:** Talep bilgileri tam (Tarih + Pax + Oda Tipi netleşti).
*   **Operasyon Kuralı:**
    *   **Min Gece Kuralı:** Önce 3 gece öner, düşük dolulukta 2 geceye in (Tent için).
    *   **Fiyatlandırma:** Etkinlik dönemi (Kids Week vb.) mi? Ödeme tipi (Nakit/Kart) ne olacak?
*   **Çıktı:**
    *   Misafire: Fiyat + Dahil Olanlar + İptal Şartlarını içeren **Teklif E-postası**.
    *   İç Ekip: "Teklif Gönderildi" işareti.

---

### C) Ön Ödeme ve Kesinleştirme (Confirmation)
**Amaç:** Opsiyonlu rezervasyonu kesin (Confirmed) statüsüne çekmek.

*   **Tetikleyici:** Misafir "Onaylıyorum" dedi veya dekont gönderdi.
*   **Operasyon Kuralı:**
    *   Onay geldiyse: Elektra'da statüyü `Option` -> `Confirmed` yap.
    *   Dekont yoksa: X saat sonra nazikçe hatırlat.
*   **Çıktı:**
    *   Misafire: "Rezervasyonunuz onaylandı/kesinleşti" mesajı.
    *   İç Ekip: Check-in hazırlık süreci başlar.

---

### D) Pre-Arrival Bilgilendirme (Guest Info Pack)
**Amaç:** Misafir gelmeden önce tüm soru işaretlerini gidermek (Konum, Kurallar, Transfer).

*   **Zamanlama:** Check-in'den **7 gün** ve **3 gün** önce.
*   **İçerik:**
    *   Konum & Yol Tarifi.
    *   Tesis Kuralları (Müzik saati, sessizlik vb.).
    *   "Ne getirmeli?" listesi.
    *   Varsa Transfer talep formu linki.
*   **Kural:** Aynı paket 2 kere gitmemeli (Idempotency).

---

### E) Transfer Talebi Yönetimi
**Amaç:** Misafiri sorunsuz şekilde tesise ulaştırmak.

*   **Tetikleyici:** PowerApp formu veya Direkt Mesaj (DM).
*   **Gerekli Bilgiler:** Güzergah, Uçuş No, Saat, Pax, Özel İhtiyaç.
*   **Araç Seçim Kuralı:**
    *   1-3 Kişi: **Taksi**
    *   4-7 Kişi: **Van (Vito)**
    *   8-13 Kişi: **Sprinter**
*   **Fiyatlandırma:**
    *   **Dalaman:** Ofis şefinin belirlediği sabit liste.
    *   **Bodrum/Diğer:** Tedarikçiden (Medusa Transfer) fiyat sorulur.
*   **Çıktı:**
    *   Tedarikçiye: Net İş Emri (Transfer Order).
    *   Misafire: "Transferiniz ayarlandı" teyidi.

---

### F) Check-In Operasyonu
**Amaç:** Hızlı ve sıcak bir karşılama.

*   **Tetikleyici:** Misafir kapıdan girdi.
*   **Kontrol:** Kimlik/Pasaport alındı mı? Oda hazır mı?
*   **Kural:** Oda hazır değilse bekleme alanına al, tahmini süre (ETA) ver.
*   **Log:** PowerApps üzerinden "Check-in Task" tamamlandı olarak işaretle.

---

### G) Check-Out ve Sonrası (Feedback)
**Amaç:** Misafiri güzel uğurlamak ve deneyimini ölçmek.

*   **Tetikleyici:** Çıkış günü.
*   **İşlem:** Folio kapatma, (varsa) hasar kontrolü.
*   **Otomasyon:** Çıkıştan **24-48 saat sonra** otomatik "Teşekkür & Geri Bildirim" e-postası gönder.

---

### H) Hazır Yanıt Kütüphanesi (IG/WhatsApp)
**Amaç:** Sık sorulan sorulara (SSS) hızlı ve standart yanıt vermek.

*   **Kullanım:** Fiyat, Çocuk Politikası, Evcil Hayvan, Müzik gibi konularda önceden onaylanmış şablonları kullan.
*   **Yönlendirme:** "Rezervasyon talebi için lütfen şu formu doldurun" diyerek akışı A maddesine bağla.

---

## 🚀 Önerilen Otomasyon Stratejisi

1.  **Microsoft Power Automate:** Eğer hali hazırda PowerApps kullanıyorsanız en doğal seçim. Outlook ve Excel ile %100 uyumlu.
2.  **n8n:** Daha esnek, özelleştirilebilir ve maliyet etkin bir çözüm. (Bizim kurduğumuz altyapı buna uygun).
3.  **Bonjuk Ops App (Hediye Ettiğimiz):** Yukarıdaki kuralların (özellikle A ve E maddeleri) şablonlarını ve hesaplamalarını sizin için otomatik yapar.
