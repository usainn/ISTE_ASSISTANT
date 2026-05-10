import requests
from bs4 import BeautifulSoup
import re
import datetime
import json
import urllib3

# SSL uyarılarını kapat
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_menu():
    url = "https://yemekhane.iste.edu.tr/"
    post_url = "https://yemekhane.iste.edu.tr/menuGetir"
    
    try:
        session = requests.Session()
        # Ana sayfayı alıp token'ı bulalım
        response = session.get(url, verify=False, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # Script içindeki token'ı bul
        script_text = ""
        for script in soup.find_all("script"):
            if "_token" in script.text:
                script_text = script.text
                break
        
        # Token regex - Hem tek hem çift tırnak destekler
        token_match = re.search(r'["\']_token["\']:\s*["\']([^"\']+)["\']', script_text)
            
        if not token_match:
            return "Menüye şu an ulaşılamıyor"

        token = token_match.group(1)
        
        # Bugünün tarihini al
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Menüyü getir
        data = {
            "tarih": today,
            "_token": token
        }
        
        post_response = session.post(post_url, data=data, verify=False, timeout=10)
        post_response.raise_for_status()
        
        # Gelen veri formatı: ["Yemek1","Yemek2",...]<-->["Yemek1","Yemek2",...]
        raw_data = post_response.text
        if "<-->" not in raw_data:
            return "Bugün için yemek menüsü henüz yayınlanmamış."
            
        menuler = raw_data.split("<-->")
        menu1_list = json.loads(menuler[0])
        
        # Menüyü formatla
        formatted_menu = ""
        icons = ["🍲", "🥩", "🍚", "🍎", "🥤", "🥖", "🥣"]
        
        for i, yemek in enumerate(menu1_list):
            if yemek.strip():
                icon = icons[i] if i < len(icons) else "🔹"
                formatted_menu += f"{icon} **{yemek.strip()}**\n\n"
        
        return formatted_menu if formatted_menu else "Menü içeriği boş."

    except Exception:
        return "Menüye şu an ulaşılamıyor"

if __name__ == "__main__":
    print(get_menu())
