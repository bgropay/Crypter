#!/usr/bin/env python3
# Title.......: Crypter
# Description.: Crack Linux Password with Python
# Author......: BgRopay
# Usage.......: python3 crypter.py
# Homepage....: github.com/bgropay/crypter

import os
import crypt
import platform
import colorama

# Colors
g = colorama.Fore.LIGHTGREEN_EX # Green
b = colorama.Fore.LIGHTBLUE_EX  # Blue
c = colorama.Fore.LIGHTCYAN_EX  # Cyan
w = colorama.Fore.LIGHTWHITE_EX # White 
m = colorama.Fore.LIGHTRED_EX   # Red
r = colorama.Fore.RESET         # Reset 

# Check if the operating system is Linux
if platform.system() != 'Linux':
    print("This script is designed to run only on Linux systems.")
    sys.exit(1)

passwd_dict = {}
shadow_dict = {}

os.system("clear")

print(f"""
{m} ___    ___    _     _  ___   _____  ___    ___   {r}
{m}(  _`\ |  _`\ ( )   ( )(  _`\(_   _)(  _`\ |  _`\ {r}
{m}| ( (_)| (_) )`\`\_/'/'| |_) ) | |  | (_(_)| (_) ){r}
{m}| |  _ | ,  /   `\ /'  | ,__/' | |  |  _)_ | ,  / {r}
{m}| (_( )| |\ \    | |   | |     | |  | (_( )| |\ \ {r}
{m}(____/'(_) (_)   (_)   (_)     (_)  (____/'(_) (_){r}
{w}         Crack Linux Password with Python         {r}
{b}        https://github.com/bgropay/crypter        {r}
""")

# Enter the path to  the Passwd file
while True:
    passwd_file = input(f"{c}[»] {w}Enter the path to the Passwd file: ")
    # condition if the Passwd file is not found 
    if not os.path.isfile(passwd_file):
        print(f"{m}[-] {w}Passwd file '{passwd_file}' not found.{r}")
        continue
    break
    
# Enter the path to the Shadow file
while True:
    shadow_file = input(f"{c}[»] {w}Enter the path to the Shadow file: ")
    # Condition if the Shadow file is not found 
    if not os.path.isfile(shadow_file):
        print(f"{m}[-] {w}Shadow file '{shadow_file}' not found.{r}")
        continue
    break

# Enter the path to the Wordlist file
while True:
    input_wordlist = input(f"{c}[»] {w}Enter the path to the Wordlist file: ")
    # Condition if the wordlist file is not found 
    if not os.path.isfile(input_wordlist):
        print(f"{m}[-] {w}Wordlist file '{input_wordlist}' not found.{r}")
        continue
    break

# Output file
output_file = "hash.txt"

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

cracked_count = 0
cracked_users = []

# Wordlist
wordlist_path = input_wordlist

with open(wordlist_path, "r", encoding="latin-1", errors="ignore") as wordlist_file:
    passwords = wordlist_file.readlines()
    password_count = len(passwords)
    print(f"{b}[*] {w}Number of passwords in the wordlist file '{wordlist_path}': {password_count}{r}")

# Crack Linux Password with Crypt
for username in shadow_dict:
    hashed_password = shadow_dict[username][1]
    print(f"{g}[+] {w}Found username: {shadow_dict[username][0]}{r}")
    print(f"{b}[*] {w}Cracking the password for username: {shadow_dict[username][0]}...{r}")
    password_found = False
    for password in passwords:
        password = password.strip()
        if crypt.crypt(password, hashed_password) == hashed_password:
            print(f"{g}[+] {w}Password found for username: {username}, Password is: {password}{r}")
            cracked_users.append((username, password))
            cracked_count += 1
            password_found = True
            break
    if not password_found:
        print(f"{m}[-] {w}Password not found for username: {username}{r}")

print(f"{g}\n[+] {w}Number of usernames successfully cracked: {cracked_count}{r}")
for username, password in cracked_users:
    print(f"{g}[+] {w}Username: {username}, Password: {password}{r}")
