import os

file_passwd = "/etc/passwd"
file_shadow = "/etc/shadow"
file_output = "unshadowed.txt"

if not os.path.exists(file_passwd) or not os.path.exists(file_shadow):
    print("File /etc/passwd atau /etc/shadow tidak ada.")
else:
    dict_passwd = {}
    dict_shadow = {}

    # Membaca file /etc/passwd
    with open(file_passwd, 'r') as passwd:
        for baris in passwd:
            bagian = baris.strip().split(':')
            if len(bagian) > 1:
                dict_passwd[bagian[0]] = bagian

    # Membaca file /etc/shadow
    with open(file_shadow, 'r') as shadow:
        for baris in shadow:
            bagian = baris.strip().split(':')
            if len(bagian) > 1:
                dict_shadow[bagian[0]] = bagian

    # Menggabungkan informasi dan menulis ke file output
    with open(file_output, 'w') as output:
        for pengguna in dict_passwd:
            if pengguna in dict_shadow:
                bagian_passwd = dict_passwd[pengguna]
                bagian_shadow = dict_shadow[pengguna]
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

    # print(f"File gabungan dibuat: {file_output}")
