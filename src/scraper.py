import os
import requests
from bs4 import BeautifulSoup
import re

def clean_filename(filename):
    # Türkçe karakterleri dönüştür
    tr_map = {
        'ı': 'i', 'İ': 'i', 'ğ': 'g', 'Ğ': 'g',
        'ü': 'u', 'Ü': 'u', 'ş': 's', 'Ş': 's',
        'ö': 'o', 'Ö': 'o', 'ç': 'c', 'Ç': 'c'
    }
    for search, replace in tr_map.items():
        filename = filename.replace(search, replace)
    
    # Küçük harfe çevir
    filename = filename.lower()
    
    # Özel karakterleri ve boşlukları alt tireye çevir
    filename = re.sub(r'[^a-z0-9.]', '_', filename)
    
    # Birden fazla alt tireyi tek alt tireye çevir
    filename = re.sub(r'_+', '_', filename)
    
    return filename

def download_mevzuat():
    url = "https://iste.edu.tr/ogrenci-isleri/mevzuat"
    print(f"Bağlanılıyor: {url}")
    
    try:
        response = requests.get(url, verify=False) # SSL hatalarını önlemek için verify=False eklendi
        response.raise_for_status()
    except Exception as e:
        print(f"Sayfaya erişilirken hata oluştu: {e}")
        return
        
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Sadece iste.edu.tr domaininden gelen PDF linklerini bul
    pdf_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.lower().endswith('.pdf'):
            if not href.startswith('http'):
                # Göreceli linkleri tam linke çevir
                href = "https://iste.edu.tr" + href if href.startswith('/') else "https://iste.edu.tr/ogrenci-isleri/" + href
            
            # Kısıtlama: Sadece iste.edu.tr domaininden al
            if 'iste.edu.tr' in href:
                pdf_links.append(href)
            
    print(f"Toplam {len(pdf_links)} PDF dosyası bulundu.")
    
    # data dizinini kontrol et ve oluştur
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    for pdf_url in pdf_links:
        # Orijinal dosya adını al
        original_name = pdf_url.split('/')[-1]
        
        # İsmi temizle
        clean_name = clean_filename(original_name)
        file_path = os.path.join(data_dir, clean_name)
        
        print(f"İndiriliyor: {clean_name}")
        
        try:
            pdf_response = requests.get(pdf_url, verify=False)
            pdf_response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                f.write(pdf_response.content)
        except Exception as e:
            print(f"Hata ({clean_name}): {e}")
            
    print("\nTüm indirme işlemleri tamamlandı. Dosyalar başarıyla 'data/' klasörüne kaydedildi.")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings() 
    download_mevzuat()
