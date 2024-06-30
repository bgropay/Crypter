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

# Warna 
h = colorama.Fore.LIGHTGREEN_EX # Hijau 
b = colorama.Fore.LIGHTBLUE_EX  # Biru 
c = colorama.Fore.LIGHTCYAN_EX  # Cyan
p = colorama.Fore.LIGHTWHITE_EX # Putih 
m = colorama.Fore.LIGHTRED_EX   # Merah 
r = colorama.Fore.RESET         # Reset 

# Periksa apakah sistem operasinya Linux
if platform.system() != 'Linux':
    print("This script is designed to run only on Linux systems.")
    sys.exit(1)

# Masukkan jalur ke file Passwd
while True:
    try:
        file_passwd = input(f"{c}[»] {p}Masukkan jalur ke file Passwd (contoh: /etc/passwd): ")
        # kondisi jika file Passwd tidak ditemukan
        if not os.path.isfile(file_passwd):
            print(f"{m}[-] {p}File Passwd '{file_passwd}' tidak ditemukan.{r}")
            continue
        break
    except KeyboardInterrupt:
        print(f"\n{m}[-] {p}Berhenti...{r}")
        exit(1)
    
# Masukkan jalur ke file Shadow 
while True:
    try:
        file_shadow = input(f"{c}[»] {p}Masukkan jalur ke file Shadow (contoh: /etc/shadow): ")
        # kondisi jika file Shadow tidak ditemukan 
        if not os.path.isfile(file_shadow):
            print(f"{m}[-] {p}File Shadow '{file_shadow}' tidak ditemukan.{r}")
            continue
        break
    except KeyboardInterrupt:
        print(f"\n{m}[-] {p}Berhenti...{r}")
        exit(1)

# Masukkan jalur ke file Wordlist 
while True:
    try:
        file_wordlist = input(f"{c}[»] {p}Masukkan jalur ke file Wordlist: ")
        # kondisi jika file Wordlist tidak ditemukan
        if not os.path.isfile(file_wordlist):
            print(f"{m}[-] {p}File wordlist '{file_wordlist}' tidak ditemukan.{r}")
            continue
        break
    except KeyboardInterrupt:
        print(f"\n{m}[-] {p}Berhenti...{r}")
        exit(1)

# Output file
output_file = "hash.txt"

passwd_dict = {}
shadow_dict = {}

# Baca file /etc/passwd
with open(file_passwd, 'r') as passwd:
    for baris in passwd:
        bagian = baris.strip().split(':')
        if len(bagian) > 1:
            nama_pengguna = bagian[0]
            gecos = bagian[4]  # Extract GECOS field
            if 'user' in gecos.lower():  # Check for 'user' in GECOS
                passwd_dict[nama_pengguna] = bagian

# Baca file /etc/shadow 
with open(shadow_file, 'r') as shadow:
    for line in shadow:
        parts = line.strip().split(':')
        if len(parts) > 1:
            username = parts[0]
            if username in passwd_dict:
                shadow_dict[username] = parts

# Gabungkan informasi untuk pengguna yang ada di kedua file
with open(output_file, 'w') as output:
    for username in passwd_dict:
        if username in shadow_dict:
            passwd_parts = passwd_dict[username]
            shadow_parts = shadow_dict[username]
            combined = ':'.join([
                passwd_parts[0],  # Nama pengguna 
                shadow_parts[1],  # Kata sandi Hash
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
    print(f"{b}[*] {w}Jumlah kata sandi dalam file Wordlist: {b}{password_count}{r}")

for username in shadow_dict:
    hashed_password = shadow_dict[username][1]
    print(f"{g}[+] {w}Menemukan nama pengguna: {g}{shadow_dict[username][0]}{r}")
    print(f"{b}[*] {w}Meng-crack kata sandi untuk nama pengguna: {b}{shadow_dict[username][0]}{w}...{r}")
    password_found = False
    for password in passwords:
        password = password.strip()
        try:
            # Crack Kata Sandi Linux dengan Crypt
            if crypt.crypt(password, hashed_password) == hashed_password:
                print(f"{g}[+] {w}Kata sandi berhasil di-crack untuk nama pengguna: {g}{username}{w}, kata sandinya adalah: {g}{password}{r}")
                cracked_users.append((username, password))
                cracked_count += 1
                password_found = True
                break
        except KeyboardInterrupt:
            print(f"\n{m}[-] {w}Berhenti...{r}")
            exit(1)
            
    if not password_found:
        print(f"{m}[-] {w}Kata sandi gagal di-crack untuk nama pengguna: {m}{username}{r}")

print(f"{g}\n[+] {w}Jumlah nama pengguna yang berhasil di-crack: {g}{cracked_count}{r}")
for username, password in cracked_users:
    print(f"{g}[+] {w}Nama pengguna: {g}{username}{w}, kata sandi: {g}{password}{r}")
