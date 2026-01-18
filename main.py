import sys
from colorama import Fore
import ui
import auth
import config
from ai_core import AICore
from voice import VoiceManager
from commands import execute_system_command

def main():
    # Ekranı temizle ve logoyu göster
    ui.clear_screen()
    ui.print_logo()
    ui.print_status_panel("BASLANIYOR")
    
    # Kimlik doğrulama
    if not auth.authenticate():
        sys.exit(1)
    
    ui.clear_screen()
    ui.print_logo()
    ui.print_status_panel("READY")
    
    # AI motorunu başlat
    ai = AICore()
    voice_manager = VoiceManager()
    
    ui.print_system("AI motoru baslatiliyor... Lutfen bekleyin ")
    
    if ai.initialize():
        ui.print_success("AI motoru basariyla baslatildi.")
    else:
        ui.print_error("AI motoru baslatma hatasi. Devam ediliyor...")
    
    ui.print_separator()
    ui.print_system("BYTE hazir. Komutlarinizi bekliyorum.")
    ui.print_system("Yardim icin 'yardim' yazin, cikmak icin 'cikis' yazin.")
    ui.print_separator()
    
    # Ana döngü
    while True:
        try:
            ui.print_prompt()
            user_input = input().strip()
            
            if not user_input:
                continue
            
            # Sistem komutları
            if user_input.lower() in ['cikis', 'exit', 'quit', 'kapat']:
                ui.print_system("BYTE kapatiliyor. Gorusmek uzere.")
                break
            
            elif user_input.lower() in ['yardim', 'help']:
                show_help()
                continue
            
            elif user_input.lower().startswith('mod '):
                handle_mode_change(user_input, ai)
                continue
            
            elif user_input.lower() == 'temizle' or user_input.lower() == 'clear':
                ui.clear_screen()
                ui.print_logo()
                ui.print_status_panel("READY")
                continue
            elif user_input.lower() == 'gecmis temizle' or user_input.lower() == 'yeni sohbet':
                result = ai.clear_history()
                ui.print_success(result)
                continue 
            
            elif user_input.lower().startswith('ses'):
                handle_voice_command(user_input, voice_manager, ai)
                continue
            
            # Sistem komutlarını kontrol et
            sys_result = execute_system_command(user_input)
            if sys_result:
                ui.print_response(sys_result)
                continue
            
            # AI'ya gönder
            if ai.is_initialized:
                ui.print_system("Dusunuyorum...")
                response = ai.get_response(user_input)
                ui.print_response(response)
            else:
                ui.print_error("AI motoru aktif degil.")
        
        except KeyboardInterrupt:
            ui.print_system("\nKesme algilandi. Cikmak icin 'cikis' yazin.")
        except Exception as e:
            ui.print_error(f"Beklenmeyen hata: {str(e)}")

def show_help():
    help_text = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                      BYTE YARDIM MENUSU                      ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  GENEL KOMUTLAR:                                             ║
    ║    yardim / help          - Bu menuyu goster                 ║
    ║    cikis / exit           - Programi kapat                   ║
    ║    temizle / clear        - Ekrani temizle                   ║
    ║    konum: (yol)                                              ║                      
    ║  MOD AYARLARI:                                               ║
    ║    mod ciddiyet [0-100]   - Ciddiyet seviyesi                ║
    ║    mod samimiyet [0-100]  - Samimiyet seviyesi               ║
    ║    mod enerji [0-100]     - Enerji seviyesi                  ║
    ║                                                              ║
    ║  SES KOMUTLARI:                                              ║
    ║    ses dinle              - Sesli komut al                   ║
    ║    ses oku [metin]        - Metni sesli oku                  ║
    ║                                                              ║
    ║  HAFIZA:                                                     ║
    ║    bunu hatirla: bilgi    - Bilgiyi hafizaya kaydet          ║
    ║    hafiza                 - Hafizayi goruntule               ║
    ║                                                              ║
    ║  SISTEM:                                                     ║
    ║    notepad                - Not Defteri ac                   ║
    ║    hesap makinesi         - Hesap Makinesi ac                ║
    ║    explorer               - Dosya Gezgini ac                 ║
    ║    paint                  - Paint ac                         ║
    ║                                                              ║
    ║  AI SOHBET:                                                  ║
    ║    Herhangi bir soru sorun veya gorev verin                  ║
    ║    Ornek: "Python'da liste olustur"                          ║
    ║    Ornek: "Bu kodu duzelt: [kod]"                            ║
    ║                                                              ║                 
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(Fore.CYAN + help_text)

def handle_mode_change(command, ai):
    parts = command.split()
    if len(parts) < 3:
        ui.print_error("Kullanim: mod [ciddiyet/samimiyet/enerji] [0-100]")
        return
    
    mode_name = parts[1].lower()
    try:
        value = int(parts[2])
        if value < 0 or value > 100:
            ui.print_error("Deger 0-100 arasinda olmalidir.")
            return
        
        if ai.update_settings(mode_name, value):
            ui.print_success(f"{mode_name.capitalize()} seviyesi %{value} olarak ayarlandi.")
        else:
            ui.print_error(f"Gecersiz mod adi: {mode_name}")
    except ValueError:
        ui.print_error("Gecersiz deger. Sayi giriniz.")

def handle_voice_command(command, voice_manager, ai):
    if "dinle" in command.lower():
        ui.print_system("Sesli komut aliniyor...")
        text = voice_manager.listen()
        if text:
            ui.print_system(f"Algilanan: {text}")
            if ai.is_initialized:
                response = ai.get_response(text)
                ui.print_response(response)
                voice_manager.speak(response)
            else:
                ui.print_error("AI motoru aktif degil.")
        else:
            ui.print_error("Ses algilanamadi.")
    
    elif "oku" in command.lower():
        text = command.replace("ses oku", "").strip()
        if text:
            voice_manager.speak(text)
            ui.print_success("Metin seslendirildi.")
        else:
            ui.print_error("Okunacak metin bulunamadi.")

if __name__ == "__main__":
    main()