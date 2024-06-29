import os

# Path file passwd dan shadow
file_passwd = "/etc/passwd"
file_shadow = "/etc/shadow"
file_output = "unshadowed_user.txt"

# Mengecek keberadaan file passwd dan shadow
if not os.path.exists(file_passwd) or not os.path.exists(file_shadow):
    print("[-] File /etc/passwd atau /etc/shadow tidak ada.")
else:
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

    print(f"[+] File gabungan berhasil dibuat: {file_output}")
