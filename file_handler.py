import os

def read_file(file_path):
    """Dosya içeriğini oku"""
    try:
        if not os.path.exists(file_path):
            return None, "Dosya bulunamadi."
        
        # Dosya uzantısını kontrol et
        ext = os.path.splitext(file_path)[1].lower()
        
        # Metin tabanlı dosyalar için
        if ext in ['.py', '.txt', '.js', '.java', '.cpp', '.c', '.cs', '.json', '.xml', '.html', '.css', '.md']:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content, None
        else:
            return None, f"Desteklenmeyen dosya turu: {ext}"
            
    except PermissionError:
        return None, "Dosya erisim izni reddedildi."
    except Exception as e:
        return None, f"Dosya okuma hatasi: {str(e)}"

def write_file(file_path, content):
    """Dosyaya yaz"""
    try:
        # Dizini oluştur (yoksa)
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, None
    except Exception as e:
        return False, f"Dosya yazma hatasi: {str(e)}"

def list_files(directory):
    """Dizindeki dosyaları listele"""
    try:
        if not os.path.exists(directory):
            return None, "Dizin bulunamadi."
        
        files = []
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            if os.path.isfile(full_path):
                files.append(item)
        
        return files, None
    except Exception as e:
        return None, f"Dizin okuma hatasi: {str(e)}"

def extract_file_path(message):
    """Mesajdan dosya yolunu çıkar"""
    keywords = ["konum:", "dosya:", "path:", "yol:"]
    
    for keyword in keywords:
        if keyword in message.lower():
            parts = message.lower().split(keyword)
            if len(parts) > 1:
                path = parts[1].strip().split()[0]
                return path
    
    # Eğer \ veya / içeren bir yol varsa
    words = message.split()
    for word in words:
        if '\\' in word or '/' in word:
            # Dosya yolu gibi görünüyor
            if any(word.endswith(ext) for ext in ['.py', '.txt', '.js', '.java', '.cpp', '.c', '.cs']):
                return word
    
    return None