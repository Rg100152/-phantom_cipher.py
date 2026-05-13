#!/usr/bin/env python3
"""
╔══════════════════════════════════════╗
║        CUI-ENCRYPT v1.0             ║
║   Terminal Encryption Suite         ║
║   AES + Caesar + Base64 + SHA256    ║
╚══════════════════════════════════════╝
"""

import base64
import hashlib
import os
import time
from getpass import getpass

# ============================================
# COLOR CODES (Terminal Styling)
# ============================================
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'

# ============================================
# BANNER
# ============================================
def show_banner():
    print(f"""{CYAN}
    ╔══════════════════════════════════════╗
    ║          CUI-ENCRYPT v1.0           ║
    ║     Terminal Encryption Suite       ║
    ╚══════════════════════════════════════╝{RESET}
    {RED}Author: CUI Team | Type 'help' for commands{RESET}
    """)

# ============================================
# CAESAR CIPHER (Shift Encryption)
# ============================================
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# ============================================
# BASE64 ENCODE / DECODE
# ============================================
def base64_encode(text):
    return base64.b64encode(text.encode()).decode()

def base64_decode(text):
    return base64.b64decode(text.encode()).decode()

# ============================================
# HASH GENERATOR
# ============================================
def generate_hash(text, algo):
    if algo == 'md5':
        return hashlib.md5(text.encode()).hexdigest()
    elif algo == 'sha1':
        return hashlib.sha1(text.encode()).hexdigest()
    elif algo == 'sha256':
        return hashlib.sha256(text.encode()).hexdigest()
    elif algo == 'sha512':
        return hashlib.sha512(text.encode()).hexdigest()
    return "Invalid Algorithm"

# ============================================
# XOR ENCRYPTION (with key)
# ============================================
def xor_encrypt(text, key):
    result = ""
    for i in range(len(text)):
        result += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return result

def xor_encrypt_hex(text, key):
    encrypted = xor_encrypt(text, key)
    return encrypted.encode().hex()

def xor_decrypt_hex(hex_text, key):
    text = bytes.fromhex(hex_text).decode()
    return xor_encrypt(text, key)  # XOR is reversible with same key

# ============================================
# REVERSE STRING
# ============================================
def reverse_string(text):
    return text[::-1]

# ============================================
# LOADING ANIMATION
# ============================================
def loading_animation(duration=1):
    print(f"{YELLOW}[*] Processing", end="")
    for _ in range(duration * 3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print(f" Done!{RESET}\n")

# ============================================
# MENU
# ============================================
def show_menu():
    print(f"""
{GREEN}╔══════════════════════ MENU ══════════════════════╗
║  {WHITE}1. Caesar Cipher Encrypt{RESET}                     {GREEN}║
║  {WHITE}2. Caesar Cipher Decrypt{RESET}                     {GREEN}║
║  {WHITE}3. Base64 Encode{RESET}                              {GREEN}║
║  {WHITE}4. Base64 Decode{RESET}                              {GREEN}║
║  {WHITE}5. Hash Generator{RESET}                             {GREEN}║
║  {WHITE}6. XOR Encrypt (Hex Output){RESET}                   {GREEN}║
║  {WHITE}7. XOR Decrypt (Hex Input){RESET}                    {GREEN}║
║  {WHITE}8. Reverse String{RESET}                             {GREEN}║
║  {WHITE}9. Full Encryption (Multi-layer){RESET}              {GREEN}║
║  {WHITE}10. Brute-Force Caesar (Simulation){RESET}           {GREEN}║
║  {WHITE}0. Exit{RESET}                                      {GREEN}║
╚══════════════════════════════════════════════════╝{RESET}
""")

# ============================================
# MULTI-LAYER ENCRYPTION
# ============================================
def multi_layer_encrypt(text, shift, xor_key):
    print(f"{BLUE}[Phase 1] Caesar Cipher...{RESET}")
    step1 = caesar_encrypt(text, shift)
    print(f"  -> {step1}")
    
    print(f"{BLUE}[Phase 2] Base64 Encoding...{RESET}")
    step2 = base64_encode(step1)
    print(f"  -> {step2}")
    
    print(f"{BLUE}[Phase 3] XOR Encryption...{RESET}")
    step3 = xor_encrypt_hex(step2, xor_key)
    print(f"  -> {step3}")
    
    return step3

def multi_layer_decrypt(hex_text, shift, xor_key):
    print(f"{BLUE}[Phase 1] XOR Decryption...{RESET}")
    step1 = xor_decrypt_hex(hex_text, xor_key)
    print(f"  -> {step1}")
    
    print(f"{BLUE}[Phase 2] Base64 Decoding...{RESET}")
    step2 = base64_decode(step1)
    print(f"  -> {step2}")
    
    print(f"{BLUE}[Phase 3] Caesar Decryption...{RESET}")
    step3 = caesar_decrypt(step2, shift)
    print(f"  -> {step3}")
    
    return step3

# ============================================
# BRUTE FORCE CAESAR (Simulation)
# ============================================
def brute_force_caesar(text):
    print(f"\n{YELLOW}[*] Attempting Brute-Force Decryption...{RESET}\n")
    loading_animation(1)
    
    for shift in range(1, 26):
        decrypted = caesar_decrypt(text, shift)
        print(f"{WHITE}Shift {shift:2d}: {GREEN}{decrypted}{RESET}")
        time.sleep(0.05)
    
    print(f"\n{YELLOW}[!] Check all 25 possibilities manually.{RESET}")

# ============================================
# MAIN FUNCTION
# ============================================
def main():
    # Clear screen (works in Pydroid terminal)
    os.system('clear' if os.name != 'nt' else 'cls')
    
    show_banner()
    
    while True:
        show_menu()
        choice = input(f"{CYAN}[cui@encrypt]~# {RESET}").strip()
        
        if choice == '0':
            print(f"\n{RED}[!] Exiting CUI-Encrypt... Stay Secure!{RESET}\n")
            break
            
        elif choice == '1':
            text = input(f"{YELLOW}[?] Text: {RESET}")
            shift = int(input(f"{YELLOW}[?] Shift (1-25): {RESET}"))
            loading_animation(0.5)
            result = caesar_encrypt(text, shift)
            print(f"{GREEN}[✓] Encrypted: {result}{RESET}\n")
            
        elif choice == '2':
            text = input(f"{YELLOW}[?] Encrypted Text: {RESET}")
            shift = int(input(f"{YELLOW}[?] Shift (1-25): {RESET}"))
            loading_animation(0.5)
            result = caesar_decrypt(text, shift)
            print(f"{GREEN}[✓] Decrypted: {result}{RESET}\n")
            
        elif choice == '3':
            text = input(f"{YELLOW}[?] Text: {RESET}")
            loading_animation(0.5)
            result = base64_encode(text)
            print(f"{GREEN}[✓] Base64: {result}{RESET}\n")
            
        elif choice == '4':
            text = input(f"{YELLOW}[?] Base64 Text: {RESET}")
            loading_animation(0.5)
            try:
                result = base64_decode(text)
                print(f"{GREEN}[✓] Decoded: {result}{RESET}\n")
            except:
                print(f"{RED}[✗] Invalid Base64!{RESET}\n")
                
        elif choice == '5':
            text = input(f"{YELLOW}[?] Text: {RESET}")
            print(f"{CYAN}Algorithms: md5 | sha1 | sha256 | sha512{RESET}")
            algo = input(f"{YELLOW}[?] Algorithm: {RESET}").lower().strip()
            loading_animation(0.5)
            result = generate_hash(text, algo)
            print(f"{GREEN}[✓] {algo.upper()}: {result}{RESET}\n")
            
        elif choice == '6':
            text = input(f"{YELLOW}[?] Text: {RESET}")
            key = getpass(f"{YELLOW}[?] XOR Key: {RESET}")
            loading_animation(0.5)
            result = xor_encrypt_hex(text, key)
            print(f"{GREEN}[✓] XOR Encrypted: {result}{RESET}\n")
            
        elif choice == '7':
            hex_text = input(f"{YELLOW}[?] Hex Text: {RESET}")
            key = getpass(f"{YELLOW}[?] XOR Key: {RESET}")
            loading_animation(0.5)
            try:
                result = xor_decrypt_hex(hex_text, key)
                print(f"{GREEN}[✓] XOR Decrypted: {result}{RESET}\n")
            except:
                print(f"{RED}[✗] Invalid Hex or Key!{RESET}\n")
                
        elif choice == '8':
            text = input(f"{YELLOW}[?] Text: {RESET}")
            loading_animation(0.5)
            result = reverse_string(text)
            print(f"{GREEN}[✓] Reversed: {result}{RESET}\n")
            
        elif choice == '9':
            text = input(f"{YELLOW}[?] Text: {RESET}")
            shift = int(input(f"{YELLOW}[?] Caesar Shift (1-25): {RESET}"))
            key = getpass(f"{YELLOW}[?] XOR Key: {RESET}")
            print()
            loading_animation(1.5)
            result = multi_layer_encrypt(text, shift, key)
            print(f"\n{GREEN}[✓] Multi-Layer Encrypted: {result}{RESET}\n")
            
        elif choice == '10':
            text = input(f"{YELLOW}[?] Encrypted Caesar Text: {RESET}")
            brute_force_caesar(text)
            print()
            
        elif choice.lower() == 'help':
            print(f"""
{CYAN}╔══════════════════ HELP ══════════════════╗
║ Commands:                                ║
║  1-10  → Select encryption method        ║
║  help  → Show this help                  ║
║  clear → Clear screen                    ║
║  0     → Exit                            ║
╚═══════════════════════════════════════════╝{RESET}
""")
            
        elif choice.lower() == 'clear':
            os.system('clear' if os.name != 'nt' else 'cls')
            show_banner()
            
        else:
            print(f"{RED}[✗] Invalid choice! Type 'help'{RESET}\n")

# ============================================
# RUN
# ============================================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{RED}[!] Interrupted! Exiting...{RESET}\n")
