import hashlib
from colorama import Fore
from config import DEFAULT_PASSWORD
import ui
import msvcrt

def get_password_with_asterisks(prompt):
    print(prompt, end='', flush=True)
    password = ""
    while True:
        char = msvcrt.getwch()
        if char == '\r':  # Enter tuşu
            print()
            break
        elif char == '\x08':  # Backspace
            if password:
                password = password[:-1]
                print('\x08 \x08', end='', flush=True)
        elif char != '\x00':  # Özel tuşlar
            password += char
            print('*', end='', flush=True)
    return password

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

STORED_PASSWORD_HASH = hash_password(DEFAULT_PASSWORD)

def authenticate():
    ui.print_system("Giris yapmak icin parolayi girin.")
    
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        password = get_password_with_asterisks(Fore.YELLOW + "    [PAROLA] > ")
        
        if hash_password(password) == STORED_PASSWORD_HASH:
            ui.print_success("Giris basarili. Hosgeldiniz.")
            return True
        else:
            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                ui.print_error(f"Yanlis parola. Kalan deneme: {remaining}")
            else:
                ui.print_error("Maksimum deneme sayisina ulasildi. Sistem kapatiliyor.")
                return False
    
    return False