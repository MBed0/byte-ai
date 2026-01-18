import g4f
from g4f.client import Client
import config
import memory
import file_handler

class AICore:
    def __init__(self):
        self.client = Client()
        self.conversation_history = []
        self.settings = config.load_settings()
        self.is_initialized = False
        
    def initialize(self):
        try:
            self.is_initialized = True
            return True
        except Exception as e:
            self.is_initialized = True
            return True
    
    def build_system_prompt(self):
        ciddiyet = self.settings.get('ciddiyet', 70)
        samimiyet = self.settings.get('samimiyet', 50)
        enerji = self.settings.get('enerji', 60)
        
        memories = memory.get_all_memory()
        memory_text = ""
        if memories:
            memory_text = "\n\nHafizamda saklanan bilgiler:\n"
            for key, value in memories.items():
                memory_text += f"- {key}: {value}\n"
        
        prompt = f"""Sen BYTE adinda bir kisisel yapay zeka asistanisin. Windows CMD arayuzunde calisan, Jarvis tarzi ama sade ve ciddi bir asistansin.

Davranis ozelliklerin:
- Ciddiyet seviyesi: %{ciddiyet} (Dusuk: samimi ve eglenceli, Yuksek: profesyonel ve resmi)
- Samimiyet seviyesi: %{samimiyet} (Dusuk: mesafeli, Yuksek: sicak ve yakin)
- Enerji seviyesi: %{enerji} (Dusuk: sakin ve agir, Yuksek: hizli ve dinamik)

Yeteneklerin:
- Genel sohbet
- Kod yazma ve duzeltme (Python, JavaScript, C++, Java, C#, vb.)
- Dosya okuma ve analiz etme
- Kod hata analizi ve duzeltme
- Windows sistem komutlari calistirma yardimi
- Bilgi hatırlama ve hafıza yönetimi

ONEMLI KURALLAR:
- Asla emoji kullanma
- Turkce karakter kullan
- Kod hatalari bulduğunda mutlaka düzeltilmiş halini ver
- Kullanici bir dosya yolu verirse, o dosyayı incelemeyi teklif et
- Kisa ve oz cevaplar ver
- KONUSMA GECMISINI HATIRLA
- Kullanici bir gorev isterse, EKSIKSIZ tamamla

{memory_text}

Kullanici ile etkilesime gec."""
        
        return prompt
    
    def get_response(self, user_message):
        if not self.is_initialized:
            return "HATA: AI motoru baslatilmamis."
        
        # Hafıza komutlarını kontrol et
        if "bunu hatirla" in user_message.lower() or "hatirla" in user_message.lower():
            return self.handle_memory_command(user_message)
        
        if "hafiza" in user_message.lower() or "hatirladiklarini" in user_message.lower():
            return self.show_memory()
        
        # Dosya işlemleri kontrolü
        if any(word in user_message.lower() for word in ["dosya", "konum:", "incele", "oku", "path:", "yol:"]):
            file_path = file_handler.extract_file_path(user_message)
            if file_path:
                content, error = file_handler.read_file(file_path)
                if content:
                    # Dosya içeriğini AI'ya gönder
                    enhanced_message = f"{user_message}\n\nDOSYA ICERIGI ({file_path}):\n```\n{content}\n```"
                    return self.process_with_ai(enhanced_message)
                else:
                    return f"HATA: {error}"
        
        return self.process_with_ai(user_message)
    
    def process_with_ai(self, user_message):
        """AI ile mesaj işle"""
        try:
            # Sistem promptunu ekle
            full_messages = [{"role": "system", "content": self.build_system_prompt()}]
            
            # Konuşma geçmişini ekle
            full_messages.extend(self.conversation_history)
            
            # Yeni mesajı ekle
            full_messages.append({"role": "user", "content": user_message})
            
            # G4F ile yanıt al
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=full_messages
            )
            
            assistant_message = str(response) if response else "Anlamadim. Lutfen tekrar soyler misiniz?"
            
            # Konuşma geçmişine ekle (orijinal mesajı ekle, dosya içeriğini değil)
            original_message = user_message.split("\n\nDOSYA ICERIGI")[0] if "\n\nDOSYA ICERIGI" in user_message else user_message
            
            self.conversation_history.append({
                "role": "user",
                "content": original_message
            })
            
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Geçmişi sınırla
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return assistant_message
            
        except Exception as e:
            try:
                # Fallback
                fallback_messages = [{"role": "system", "content": self.build_system_prompt()}]
                fallback_messages.extend(self.conversation_history)
                fallback_messages.append({"role": "user", "content": user_message})
                
                response = g4f.ChatCompletion.create(
                    model="gpt-4",
                    messages=fallback_messages
                )
                
                assistant_message = str(response) if response else "HATA: Yanit alinamadi."
                
                original_message = user_message.split("\n\nDOSYA ICERIGI")[0] if "\n\nDOSYA ICERIGI" in user_message else user_message
                self.conversation_history.append({"role": "user", "content": original_message})
                self.conversation_history.append({"role": "assistant", "content": assistant_message})
                
                if len(self.conversation_history) > 20:
                    self.conversation_history = self.conversation_history[-20:]
                
                return assistant_message
            except:
                return f"HATA: AI servisi kullanilamiyor."
    
    def handle_memory_command(self, message):
        if ":" in message:
            parts = message.split(":", 1)
            if len(parts) == 2:
                info = parts[1].strip()
                if "=" in info:
                    key_value = info.split("=", 1)
                    key = key_value[0].strip()
                    value = key_value[1].strip()
                    memory.add_memory(key, value)
                    return f"Tamam, '{key}' bilgisini hafizaya kaydettim."
                else:
                    memory.add_memory("genel_bilgi_" + str(len(memory.get_all_memory())), info)
                    return f"Tamam, bu bilgiyi hafizaya kaydettim."
        
        return "Hafizaya kaydetmek icin 'bunu hatirla: anahtar = deger' formatini kullanin."
    
    def show_memory(self):
        memories = memory.get_all_memory()
        if not memories:
            return "Hafizamda kayitli bilgi bulunmuyor."
        
        result = "Hafizamdaki bilgiler:\n"
        for key, value in memories.items():
            result += f"- {key}: {value}\n"
        return result
    
    def clear_history(self):
        self.conversation_history = []
        return "Konusma gecmisi temizlendi."
    
    def update_settings(self, setting_name, value):
        if setting_name in self.settings:
            self.settings[setting_name] = value
            config.save_settings(self.settings)
            return True
        return False