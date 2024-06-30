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
import sys

# Colors
g = colorama.Fore.LIGHTGREEN_EX # Green
b = colorama.Fore.LIGHTBLUE_EX  # Blue
c = colorama.Fore.LIGHTCYAN_EX  # Cyan
w = colorama.Fore.LIGHTWHITE_EX # White 
m = colorama.Fore.LIGHTRED_EX   # Red
r = colorama.Fore.RESET         # Reset 

def check_os():
    if platform.system() != 'Linux':
        print("This script is designed to run only on Linux systems.")
        sys.exit(1)

def check_file_exists(filepath, filetype):
    if not os.path.isfile(filepath):
        print(f"{m}[-] {w}{filetype} file '{filepath}' not found.{r}")
        sys.exit(1)

def get_input_filepath(prompt, filetype):
    while True:
        input_filepath = input(f"{c}[»] {w}{prompt}: ")
        if not os.path.isfile(input_filepath):
            print(f"{m}[-] {w}{filetype} file '{input_filepath}' not found.{r}")
            continue
        return input_filepath

def read_passwd_file(passwd_file):
    passwd_dict = {}
    with open(passwd_file, 'r') as passwd:
        for line in passwd:
            parts = line.strip().split(':')
            if len(parts) > 1:
                username = parts[0]
                gecos = parts[4]  # Extract GECOS field
                if 'user' in gecos.lower():  # Check for 'user' in GECOS
                    passwd_dict[username] = parts
    return passwd_dict

def read_shadow_file(shadow_file, passwd_dict):
    shadow_dict = {}
    with open(shadow_file, 'r') as shadow:
        for line in shadow:
            parts = line.strip().split(':')
            if len(parts) > 1:
                username = parts[0]
                if username in passwd_dict:
                    shadow_dict[username] = parts
    return shadow_dict

def combine_info(passwd_dict, shadow_dict, output_file):
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

def crack_passwords(shadow_dict, wordlist_path):
    cracked_count = 0
    cracked_users = []

    with open(wordlist_path, "r", encoding="latin-1", errors="ignore") as wordlist_file:
        passwords = wordlist_file.readlines()
        password_count = len(passwords)
        print(f"{b}[*] {w}Number of passwords in the wordlist file '{wordlist_path}': {password_count}{r}")

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

def main():
    check_os()

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

    passwd_file = get_input_filepath("Enter the path to the Passwd file", "Passwd")
    shadow_file = get_input_filepath("Enter the path to the Shadow file", "Shadow")
    input_wordlist = get_input_filepath("Enter the path to the Wordlist file", "Wordlist")
    
    passwd_dict = read_passwd_file(passwd_file)
    shadow_dict = read_shadow_file(shadow_file, passwd_dict)
    combine_info(passwd_dict, shadow_dict, "hash.txt")
    crack_passwords(shadow_dict, input_wordlist)

if __name__ == "__main__":
    main()
