# Bonjuk Bay Operasyonel Mail Formatları 🧿

Bu doküman, Bonjuk Bay'in profesyonel ve sıcak iletişim dilini korumak, aynı zamanda otomasyon sisteminin (AI Parsing) verileri hatasız okumasını sağlamak için hazırlanmıştır.

---

## 1. Yeni Rezervasyon Talebi (Sistem Çıktısı)
Web sitesinden veya ilk temastan gelen bu format, otomasyonumuzun "ana besin" kaynağıdır.

**Konu:** [NEW REQUEST] Rezervasyon Talebi - {{Misafir_Adı}} (#{{Talep_ID}})

**Mail İçereği:**
> Dear {{Misafir_Adı}},
>
> Rezervasyon talebiniz bize ulaştı. En kısa sürede sizinle iletişime geçeceğiz.
> 
> **Rezervasyon Detayları:**
> - **Guest Name:** {{Ad_Soyad}}
> - **Id/Passport Number:** {{TC_veya_Pasaport}}
> - **Social Link:** {{Instagram_veya_LinkedIn}}
> - **Room Type:** {{Oda_Tipi}}
> - **Bed Type:** {{Yatak_Tipi}}
> - **Check-In:** {{DD.MM.YYYY}}
> - **Check-Out:** {{DD.MM.YYYY}}
> - **Pax (Kişi Sayısı):** {{Sayı}}
> - **Message:** {{Misafir_Notu}}
>
> Teşekkürler,
> Bonjuk Bay Team 🧿

---

## 2. Eksik Bilgi Talep Maili (Asistan Çıktısı)
Dashboard üzerinden "Eksik Bilgi Bildir" butona basıldığında üretilen taslak.

**Konu:** Rezervasyon Talebi Hakkında Önemli Not - {{Misafir_Adı}}

**Mail İçeriği:**
> Selam {{Misafir_Adı}},
>
> Talebiniz için çok heyecanlıyız! 🧿 Ancak size en uygun teklifi hazırlayabilmemiz için minik bir bilgiye daha ihtiyacımız var:
> 
> **Eksik Alan:** {{Eksik_Alan_Adı}} (Örn: Giriş tarihi veya Pax sayısı)
>
> Bu bilgiyi bizimle paylaşırsanız teklifinizi hemen ileteceğiz.
>
> Warm hugs! 🕯️✨
> {{Kullanıcı_Adı}}

---

## 3. Konfirmasyon ve Ödeme Talebi
Rezervasyon onaylandığında misafire giden "Final" format.

**Konu:** Rezervasyon Konfirmasyonu: {{Giriş_Tarihi}} - {{Misafir_Adı}}

**Mail İçeriği:**
> Selam {{Misafir_Adı}},
>
> Sizi aramızda görmek için sabırsızlanıyoruz! 🧿 Rezervasyonunuzu 24 saatliğine opsiyonladık. Kaydınızın tamamlanması için aşağıdaki ödeme detaylarını takip etmenizi rica ederiz.
>
> **Özet Detaylar:**
> - **Tarih:** {{Giriş}} - {{Çıkış}}
> - **Oda:** {{Oda_Tipi}}
> - **Tutar:** {{Tutar}} {{Para_Birimi}}
>
> **Ödeme Linki:** {{PayTR_veya_NEXORDO_Link}}
>
> **IBAN Detayları:**
> [IBAN BİLGİLERİ BURAYA]
>
> Görüşmek üzere! 🌞
> Warm hugs,
> {{Kullanıcı_Adı}}
---

## 4. [EN] New Reservation Request
Automatic format for international guests.

**Subject:** [NEW REQUEST] Reservation Request - {{Guest_Name}} (#{{Request_ID}})

**Body:**
> Dear {{Guest_Name}},
>
> Your reservation request has reached us. We will contact you as soon as possible.
> 
> **Reservation Details:**
> - **Guest Name:** {{Full_Name}}
> - **Id/Passport Number:** {{Passport_No}}
> - **Social Link:** {{Instagram_or_LinkedIn}}
> - **Room Type:** {{Room_Type}}
> - **Bed Type:** {{Bed_Type}}
> - **Check-In:** {{DD.MM.YYYY}}
> - **Check-Out:** {{DD.MM.YYYY}}
> - **Pax (Number of Guests):** {{Count}}
> - **Message:** {{Guest_Note}}
>
> Thank you for choice... 
> Bonjuk Bay Team 🧿

---

## 5. [EN] Missing Information Request
Draft for when a profile is incomplete.

**Subject:** Important Note Regarding Your Reservation Request - {{Guest_Name}}

**Body:**
> Hi {{Guest_Name}},
>
> We are so excited about your request! 🧿 However, we need one more little piece of information to prepare the best offer for you:
> 
> **Missing Information:** {{Field_Name}} (e.g., Check-in date or Pax count)
>
> Once you share this with us, we will send your offer immediately.
>
> Warm hugs! 🕯️✨
> {{User_Name}}

---

## 6. [EN] Confirmation & Payment Request
Final format for international approvals.

**Subject:** Reservation Confirmation: {{Check-In_Date}} - {{Guest_Name}}

**Body:**
> Hi {{Guest_Name}},
>
> We can't wait to see you with us! 🧿 We have optioned your reservation for 24 hours. To complete your registration, please follow the payment details below.
>
> **Summary Details:**
> - **Dates:** {{Check-In}} - {{Check-Out}}
> - **Room:** {{Room_Type}}
> - **Amount:** {{Amount}} {{Currency}}
>
> **Payment Link:** {{Payment_Link}}
>
> **International Bank Details (SWIFT):**
> [SWIFT DETAILS HERE]
>
> See you soon! 🌞
> Warm hugs,
> {{User_Name}}
