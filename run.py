import crypt

crypt3_hash = input("Masukkan hash crypt(3) yang ingin di-crack: ").strip()
wordlist_file = input("Masukkan nama file wordlist: ").strip()

with open(wordlist_file, 'r') as f:
    for password in f.readlines():
        password = password.strip()
        # Generate hash with the same salt as in crypt3_hash
        if crypt.crypt(password, crypt3_hash) == crypt3_hash:
            print(f"Password berhasil di-crack: {password}")
            break
    else:
        print("Password tidak ditemukan dalam wordlist.")
      
