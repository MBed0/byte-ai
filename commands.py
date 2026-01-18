import subprocess
import os

def execute_system_command(command):
    command_lower = command.lower()
    
    # Uygulama açma
    if "notepad" in command_lower or "not defteri" in command_lower:
        subprocess.Popen("notepad.exe")
        return "Not Defteri acildi."
    
    elif "hesap makinesi" in command_lower or "calculator" in command_lower:
        subprocess.Popen("calc.exe")
        return "Hesap Makinesi acildi."
    
    elif "chrome" in command_lower:
        try:
            subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"])
            return "Chrome tarayici acildi."
        except:
            return "Chrome bulunamadi."
    
    elif "explorer" in command_lower or "dosya gezgini" in command_lower:
        subprocess.Popen("explorer.exe")
        return "Dosya Gezgini acildi."
    
    elif "cmd" in command_lower:
        subprocess.Popen("cmd.exe")
        return "Yeni CMD penceresi acildi."
    
    elif "paint" in command_lower:
        subprocess.Popen("mspaint.exe")
        return "Paint acildi."
    
    # Sistem komutları
    elif "kapat pc" in command_lower or "bilgisayari kapat" in command_lower:
        return "Guvenlik nedeniyle bu komut devre disi birakildi."
    
    return None