import requests
import urllib3

# SSL uyarılarını kapat
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_iskenderun_weather():
    """
    wttr.in kullanarak İskenderun hava durumunu çeker.
    """
    url = "https://wttr.in/Iskenderun?format=%C+%t"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        return "Hava durumu bilgisi alınamadı."
    except Exception:
        return "Hava durumu bilgisi alınamadı."

def get_detailed_weather():
    """
    Daha detaylı hava durumu bilgisi döner (Sıcaklık ve Açıklama).
    """
    try:
        # Örn: "Clear +25°C"
        weather_text = get_iskenderun_weather()
        
        # İngilizce terimleri Türkçeye çevirelim (basit bir eşleme)
        translate = {
            "Clear": "Açık ☀️",
            "Sunny": "Güneşli ☀️",
            "Partly cloudy": "Parçalı Bulutlu ⛅",
            "Cloudy": "Bulutlu ☁️",
            "Overcast": "Kapalı ☁️",
            "Mist": "Sisli 🌫️",
            "Patchy rain possible": "Yer yer yağmurlu 🌦️",
            "Rain": "Yağmurlu 🌧️",
            "Light rain": "Hafif Yağmurlu 🌧️",
            "Thunderstorm": "Fırtınalı ⛈️"
        }
        
        for eng, tr in translate.items():
            if eng in weather_text:
                weather_text = weather_text.replace(eng, tr)
        
        return weather_text
    except:
        return "İskenderun: Bilgi yok"

if __name__ == "__main__":
    print(get_detailed_weather())
