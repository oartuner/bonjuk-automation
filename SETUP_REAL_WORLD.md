# 🌍 Bonjuk App: Supabase Kurulum Rehberi 🚀

Uygulamanın verileri kaydetmesi için Supabase (Bulut Veritabanı) kurulumu yapıyoruz. Bu işlem tamamen ücretsizdir.

## 1. Supabase Projesi Oluşturun
1. [supabase.com](https://supabase.com) adresine gidip "Start your project" diyerek ücretsiz üye olun.
2. "New Project" butonuna basın.
3. Proje Adı: `bonjuk-ops` (veya istediğiniz bir isim).
4. Bir şifre belirleyin ve bölge olarak "Frankfurt" veya "London" seçin (Türkiye'ye yakın).
5. "Create new project" diyip 1-2 dakika bekleyin.

## 2. Tabloyu Oluşturun
Proje açıldıktan sonra soldaki menüden **Table Editor** (Tablo simgesi) kısmına girin.
1. "New Table" butonuna basın.
2. Name: `reservations`
3. "Enable RLS" işaretini kaldırın (Şimdilik gerek yok).
4. Aşağıdaki sütunları (Columns) ekleyin:

| Name | Type |
|---|---|
| id | int8 (otomatik seçili gelir) |
| created_at | timestamptz (otomatik seçili gelir) |
| guest_name | text |
| pax | int8 |
| check_in | date |
| check_out | date |
| accommodation_type | text |
| notes | text |

5. "Save" diyerek tabloyu oluşturun.

## 3. Bağlantı Bilgilerini Alın
1. Sol menüden **Project Settings** (Dişli simgesi) > **API** kısmına gidin.
2. **Project URL** kutusundaki adresi kopyalayın.
3. **Project API keys** kısmındaki `anon` `public` key'i kopyalayın.

## 4. Uygulamaya Tanıtın
Bu iki bilgiyi projenizdeki `.env` dosyasına yapıştırın:

```properties
SUPABASE_URL=kopyaladiginiz_url_buraya
SUPABASE_KEY=kopyaladiginiz_anon_key_buraya
```

🎉 **Tebrikler!** Artık Bonjuk App üzerinden girilen her rezervasyon anında buluta kaydedilecek ve silinmeyecek.
