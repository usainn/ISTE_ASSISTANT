from datetime import datetime
import streamlit as st

# ISTE 2025-2026 Akademik Takvimi
AKADEMIK_TAKVIM = {
    "Güz Vize Sınavları": datetime(2025, 11, 15),
    "Güz Final Sınavları": datetime(2026, 1, 5),
    "Bahar Vize Sınavları": datetime(2026, 3, 28),
    "Bahar Final Sınavları": datetime(2026, 6, 1),
    "Bahar Bütünleme Sınavları": datetime(2026, 6, 15)
}

def get_countdown_info():
    bugun = datetime.now()
    
    # Gelecekteki en yakın sınavı bul
    gelecek_sinavlar = {k: v for k, v in AKADEMIK_TAKVIM.items() if v > bugun}
    
    if not gelecek_sinavlar:
        return "Şu an için takvimde bekleyen yakın bir sınav bulunmuyor.", "info"
    
    # En yakın sınavı seç
    en_yakin_sinav_adi = min(gelecek_sinavlar, key=gelecek_sinavlar.get)
    en_yakin_tarih = gelecek_sinavlar[en_yakin_sinav_adi]
    
    kalan_gun = (en_yakin_tarih - bugun).days
    
    # Mesaj ve Durum Belirleme
    if kalan_gun == 0:
        msg = f"🚀 **Bugün {en_yakin_sinav_adi} Başlıyor!** Başarılar dilerim."
        status = "error" # Kırmızı/Dikkat çekici
    elif kalan_gun < 7:
        msg = f"🚨 **{en_yakin_sinav_adi}**'na sadece **{kalan_gun}** gün kaldı! Notlarını düzenlemeye başlamak ister misin?"
        status = "warning"
    else:
        msg = f"📅 **{en_yakin_sinav_adi}**'na **{kalan_gun}** gün var. Hazırlıklara devam!"
        status = "info"
        
    return msg, status
