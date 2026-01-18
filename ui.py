import os
from colorama import init, Fore, Style

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_logo():
    logo = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║       ██████╗ ██╗   ██╗████████╗███████╗     █████╗ ██╗      ║
    ║       ██╔══██╗╚██╗ ██╔╝╚══██╔══╝██╔════╝    ██╔══██╗██║      ║
    ║       ██████╔╝ ╚████╔╝    ██║   █████╗      ███████║██║      ║
    ║       ██╔══██╗  ╚██╔╝     ██║   ██╔══╝      ██╔══██║██║      ║
    ║       ██████╔╝   ██║      ██║   ███████╗    ██║  ██║██║      ║
    ║       ╚═════╝    ╚═╝      ╚═╝   ╚══════╝    ╚═╝  ╚═╝╚═╝      ║
    ║                                                              ║                                             
    ║                                                              ║
    ║                                                              ║                                             
    ║                                                              ║
    ║                                                              ║
    ║                                                              ║
    ║              Kisisel Yapay Zeka Sistemi v1.0                 ║
    ║                      made by Byte Comp.                      ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(Fore.LIGHTWHITE_EX + logo)

def print_status_panel(status="READY"):
    panel = f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║  DURUM: {status:<20} | SISTEM: ONLINE                        ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(Fore.GREEN + panel)

def print_separator():
    print(Fore.WHITE + "    " + "="*60)

def print_prompt():
    print(Fore.YELLOW + "\n    [BYTE] ", end="")

def print_system(message):
    print(Fore.CYAN + f"    >> {message}")

def print_error(message):
    print(Fore.RED + f"    [HATA] {message}")

def print_success(message):
    print(Fore.GREEN + f"    [BASARILI] {message}")

def print_response(message):
    print(Fore.WHITE + f"\n    {message}\n")