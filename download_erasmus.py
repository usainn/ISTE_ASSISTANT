import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse, parse_qs

def iste_konu_bul_ve_indir(konu):
    search_url = "https://lite.duckduckgo.com/lite/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'q': f'site:iste.edu.tr {konu} mevzuat pdf'
    }
    
    print(f"[{konu.upper()}] konusu için İSTE web sitesinde PDF'ler taranıyor...")
    
    try:
        response = requests.post(search_url, headers=headers, data=data)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        pdf_links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            
            if href.lower().endswith('.pdf') and 'iste.edu.tr' in href:
                if href not in pdf_links:
                    pdf_links.append(href)
                    
        if not pdf_links:
            print(f"Uyarı: '{konu}' ile ilgili herhangi bir PDF bağlantısı bulunamadı.")
            return
            
        print(f"Toplam {len(pdf_links)} adet mevzuat PDF'i bulundu. İndirme başlatılıyor...\n")
        
        os.makedirs('data', exist_ok=True)
        tarih = datetime.now().strftime("%Y%m%d")
        
        for i, link in enumerate(pdf_links, 1):
            try:
                print(f"İndiriliyor [{i}/{len(pdf_links)}]: {link}")
                pdf_response = requests.get(link, headers=headers, timeout=15)
                pdf_response.raise_for_status()
                
                guvenli_konu = konu.replace(" ", "_").replace("ç", "c").replace("ş", "s").replace("ı", "i").replace("ğ", "g").replace("ö", "o").replace("ü", "u").lower()
                dosya_adi = f"data/iste_{guvenli_konu}_{tarih}_{i}.pdf"
                
                with open(dosya_adi, 'wb') as f:
                    f.write(pdf_response.content)
                    
                print(f"  -> Başarıyla kaydedildi: {dosya_adi}")
                
            except Exception as e:
                print(f"  -> İndirme hatası ({link}): {e}")
                
    except Exception as e:
        print(f"Arama işlemi sırasında sunucuya bağlanılamadı: {e}")

if __name__ == "__main__":
    iste_konu_bul_ve_indir("Erasmus")
