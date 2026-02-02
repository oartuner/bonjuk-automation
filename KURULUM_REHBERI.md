# 🧿 Bonjuk Automation - Kurulum ve Yapılandırma Rehberi

Bu rehber, projenin yerel bilgisayarda çalıştırılması ve Outlook entegrasyonunun tamamlanması için gereken adımları içerir.

---

## 🚀 1. Başlangıç (Kurulum)

Uygulamayı çalıştırmadan önce terminal (PowerShell veya CMD) üzerinden şu komutları sırasıyla çalıştırın:

1.  **Kütüphaneleri Yükleyin:**
    ```bash
    python -m pip install -r requirements.txt
    ```

2.  **Uygulamayı Başlatın:**
    ```bash
    python -m streamlit run src/app.py
    ```
    *Uygulama tarayıcınızda `http://localhost:8501` adresinde açılacaktır.*

---

## ⚙️ 2. Yapılandırma (.env Dosyası)

Projenin ana dizinindeki `.env` dosyasını bir metin düzenleyici (Notepad, VS Code vb.) ile açın ve aşağıdaki alanları doldurun:

```ini
# Outlook Ayarları
EMAIL_HOST=outlook.office365.com
EMAIL_PORT=993
EMAIL_USER=senin_mail_adresin@outlook.com
EMAIL_PASS=BURAYA_UYGULAMA_PAROLASI_GELECEK

# AI Ayarları
GEMINI_API_KEY=Senin_Gemini_API_Anahtarın
```

---

## 🔑 3. Outlook "Uygulama Parolası" Nasıl Alınır?

Outlook normal şifrenizle bu yazılıma giriş yapamazsınız (güvenlik nedeniyle engellenir). Özel bir şifre üretmeniz gerekir:

1.  [Microsoft Güvenlik Ayarları](https://account.live.com/proofs/manage/additional) sayfasına gidin ve giriş yapın.
2.  **"Gelişmiş güvenlik seçenekleri"** kısmına tıklayın.
3.  Sayfayı aşağı kaydırın ve **"Uygulama parolaları"** başlığını bulun.
4.  **"Yeni uygulama parolası oluştur"** seçeneğine tıklayın.
5.  Ekran gelen **16 karakterlik karmaşık şifreyi** kopyalayın.
6.  Bu şifreyi `.env` dosyasındaki `EMAIL_PASS` kısmına yapıştırın.

---

## 📖 4. Uygulama Modülleri

-   **Dashboard:** Gelen mailleri tarar ve simülasyon/gerçek veri akışını gösterir.
-   **Rezervasyon Talebi:** Gelen karmaşık mail metinlerini yapay zeka (Gemini) ile analiz eder; isim, tarih, kişi sayısı gibi bilgileri otomatik ayıklar.
-   **Transfer Planlayıcı:** Yolcu sayısına göre araç tipi ve fiyat tahmini yapar.
-   **Hazır Yanıtlar:** Misafirlere gönderilecek Türkçe/İngilizce onay veya eksik bilgi mesajlarını hızlıca hazırlar.

---

*Not: Herhangi bir hata durumunda `.env` dosyasındaki bilgilerin doğruluğunu ve internet bağlantısını kontrol edin.*
