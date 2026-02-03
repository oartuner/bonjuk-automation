import openpyxl
from datetime import datetime

# Excel'den etkinlik takvimini oku
wb = openpyxl.load_workbook('docs/2026 Bonjuk.xlsx')
sheet = wb['2026 Program']

print("Python kod üretiliyor...")
print("\nEVENT_CALENDAR = [")

for row in sheet.iter_rows(min_row=2, values_only=True):
    if row[0] and row[1]:  # Hem tarih hem etkinlik adı varsa
        date_range = str(row[0]).strip()
        event_name = str(row[1]).strip()
        
        # Tarih aralığını parse et (örn: "30 Nisan – 04 Mayıs")
        try:
            parts = date_range.replace('–', '-').replace('—', '-').split('-')
            if len(parts) == 2:
                start_str = parts[0].strip()
                end_str = parts[1].strip()
                
                # Türkçe ay isimlerini İngilizce'ye çevir
                month_map = {
                    'Nisan': '04', 'Mayıs': '05', 'Haziran': '06',
                    'Temmuz': '07', 'Ağustos': '08', 'Eylül': '09',
                    'Ekim': '10', 'Kasım': '11'
                }
                
                # Başlangıç tarihi
                start_parts = start_str.split()
                if len(start_parts) == 2:
                    start_day = start_parts[0]
                    start_month = month_map.get(start_parts[1], '01')
                    start_date = f"2026-{start_month}-{start_day.zfill(2)}"
                    
                    # Bitiş tarihi
                    end_parts = end_str.split()
                    if len(end_parts) == 2:
                        end_day = end_parts[0]
                        end_month = month_map.get(end_parts[1], start_month)
                    else:
                        end_day = end_str
                        end_month = start_month
                    
                    end_date = f"2026-{end_month}-{end_day.zfill(2)}"
                    
                    print(f'    {{"start": "{start_date}", "end": "{end_date}", "name": "{event_name}", "fee": None}},')
        except Exception as e:
            print(f"    # Hata: {date_range} -> {event_name}")

print("]")
