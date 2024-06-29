# Program : Menggabungkan informasi dari file /etc/passwd dan /etc/shadow pada sistem operasi Linux.
# Pembuat : BgRopay
# Github  : https://github.com/bgropay/Unshadow
# Lisensi : MIT

# Informasi
# ---------
# Program ini menggabungkan informasi dari file /etc/passwd dan /etc/shadow
# pada sistem operasi Linux. Ini mencakup username dan hash password,
# yang dapat di-crack menggunakan alat seperti John the Ripper atau Hashcat.
#
# [ Crack menggunakan John The Ripper ]
# Command: john --wordlist=/path/to/wordlist.txt [file_unshadow]

import os
import time
import datetime

while True:    
    try:
        import colorama
    except ImportError:
        print("Error: Modul colorama belum terinstal.")
        time.sleep(1)
        print("[*] Menginstal modul colorama...")
        time.sleep(3)
        os.system("python3 -m venv modules")
        os.system("source modules/bin/activate")
        os.system("pip3 install colorama")
        continue
    break

# Mengubah output warna teks
m = colorama.Fore.LIGHTRED_EX    # merah
h = colorama.Fore.LIGHTGREEN_EX  # hijau
b = colorama.Fore.LIGHTBLUE_EX   # biru
c = colorama.Fore.LIGHTCYAN_EX   # cyan
p = colorama.Fore.LIGHTWHITE_EX  # putih
r = colorama.Fore.RESET    # reset

waktu = datetime.datetime.now()
fw = waktu.strftime("%H:%M:%S")

# Path file passwd dan shadow
file_passwd = "/etc/passwd"
file_shadow = "/etc/shadow"

print(f"{p}[{c}{fw}{p}] [{h}INFO{p}] {r}Mengecek file '{file_passwd}'...{r}")
time.sleep(3)

if os.path.isfile(file_passwd):
    print(f"{p}[{c}{fw}{p}] [{h}INFO{p}] File '{file_passwd}' ditemukan.{r}")
else:
    time.sleep(2)
    print(f"{m}[-] {p}File '{file_passwd}' tidak ditemukan.{r}")
    exit(1)

print(f"{b}[*] {p}Mengecek file '{file_shadow}'...{r}")
time.sleep(3)

if os.path.isfile(file_shadow):
    print(f"{h}[+] {p}File '{file_shadow}' ditemukan.{r}")
else:
    time.sleep(2)
    print(f"{m}[-] {p}File '{file_shadow}' tidak ditemukan.{r}")
    exit(1)

try:
    file_output = input(f"{c}[»] {p}Masukkan nama file output: ")
except KeyboardInterrupt:
    print(f"\n{m}[-] {p}Keluar...{k}:({r}")
    exit(1)


dict_passwd = {}
dict_shadow = {}

# Membaca file /etc/passwd
with open(file_passwd, 'r') as passwd:
    for baris in passwd:
        bagian = baris.strip().split(':')
        if len(bagian) > 1:
            username = bagian[0]
            gecos = bagian[4]  # Mengambil bagian GECOS
            if 'user' in gecos.lower():  # Memeriksa keberadaan 'user' dalam GECOS
                dict_passwd[username] = bagian

# Membaca file /etc/shadow
with open(file_shadow, 'r') as shadow:
    for baris in shadow:
        bagian = baris.strip().split(':')
        if len(bagian) > 1:
            username = bagian[0]
            if username in dict_passwd:
                dict_shadow[username] = bagian

# Menggabungkan informasi untuk pengguna yang ada di kedua file
with open(file_output, 'w') as output:
    for username in dict_passwd:
        if username in dict_shadow:
            bagian_passwd = dict_passwd[username]
            bagian_shadow = dict_shadow[username]
            gabungan = ':'.join([
                bagian_passwd[0],  # nama pengguna
                bagian_shadow[1],  # hash kata sandi
                bagian_passwd[2],  # UID
                bagian_passwd[3],  # GID
                bagian_passwd[4],  # GECOS
                bagian_passwd[5],  # direktori
                bagian_passwd[6]   # shell
            ])
            output.write(gabungan + '\n')
print(f"{b}[*] {p}Mengcrack kata sandi Linux menggunakan John The Ripper...{r}")
time.sleep(3)
# Wordlist yang digunakan untuk meng-crack kata sandi Linux 
wordlist="/usr/share/wordlists/rockyou.txt"
# Meng-crack kata sandi Linux menggunakan Jihn The Ripper
os.system(f"john --wordlist={wordlist} {file_output}")
print(f"{p}[{c}INFO{p}] Proses cracking selesai.{r}")
print(f"{p}[{c}INFO{p}] Ketikkan 'john --show [nama file output]' untuk melihat hasil proses cracking.{r}")
exit(0)
