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

# Path file passwd dan shadow
file_passwd = "/etc/passwd"
file_shadow = "/etc/shadow"
file_output = "hash.txt"

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
# Wordlist yang digunakan untuk meng-crack kata sandi Linux 
wordlist="/usr/share/wordlists/rockyou.txt"
# Meng-crack kata sandi Linux menggunakan Jihn The Ripper
os.system(f"john --wordlist={wordlist} {file_output}")
os.system(f"john --show {file_output}")
exit(0)
