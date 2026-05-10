import os
from dotenv import load_dotenv

# Çevresel değişkenleri yükle
load_dotenv()

# Çevrimdışı mod: HuggingFace modelini sadece yerel önbellekten yükle, ağda takılmasını önle
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

# API Keys
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Klasör Yolları
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
VECTOR_DB_DIR = os.path.join(BASE_DIR, "vector_db")

# Dizinler yoksa oluştur
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VECTOR_DB_DIR, exist_ok=True)
