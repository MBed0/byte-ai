import os
import json
from dotenv import load_dotenv
load_dotenv()
APP_NAME = "BYTE"
VERSION = "1.0"
DEFAULT_PASSWORD = os.getenv("ADMIN_PASSWORD_AI", "byte2024")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

os.makedirs(DATA_DIR, exist_ok=True)

DEFAULT_SETTINGS = {
    "ciddiyet": 70,
    "samimiyet": 50,
    "enerji": 60,
    "voice_enabled": False
}

def load_settings():
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:  # Dosya boş değilse
                    return json.loads(content)
                else:
                    # Boş dosya, yeniden oluştur
                    save_settings(DEFAULT_SETTINGS)
                    return DEFAULT_SETTINGS
        else:
            # Dosya yoksa oluştur
            save_settings(DEFAULT_SETTINGS)
            return DEFAULT_SETTINGS
    except (json.JSONDecodeError, Exception) as e:
        # Hatalı JSON, yeniden oluştur
        print(f"Ayar dosyasi bozuk, yeniden olusturuluyor...")
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Ayarlar kaydedilemedi: {e}")