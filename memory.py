import json
import os
from config import MEMORY_FILE

def load_memory():
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
                else:
                    return {}
        return {}
    except (json.JSONDecodeError, Exception):
        # Hatalı dosya, boş döndür
        return {}

def save_memory(memory_data):
    try:
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Hafiza kaydedilemedi: {e}")

def add_memory(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)

def get_memory(key):
    memory = load_memory()
    return memory.get(key, None)

def get_all_memory():
    return load_memory()

def clear_memory():
    save_memory({})