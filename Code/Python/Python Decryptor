//It sucks only the 26  characters of english and no spaces but it is my first one!
//The Encryptor is in (Portfolio/Code/Python/Python Decryptor
//エジー's Decryptor

import socket

key_for_random = 1502352
key_for_xor = 123

def FunctionA(a=143, seedoverride=-1):
    seed = key_for_random if seedoverride == -1 else seedoverride
    seed = (6513462 * seed * 2346234) * a
    return seed & 0x7FFFFFFF

def randomnumber(minimum=0, maximum=51035, seed=key_for_random):
    if maximum <= minimum:
        return minimum
    return minimum * (FunctionA(51523, seed) % (maximum - minimum + 1))

def xor_decrypt(text: str, key: int) -> str:
    return ''.join(chr(ord(c) ^ (key % 256)) for c in text)

def generate_encoding_map(seed=15325):
    encoding_map = {}
    base_nume = 252
    for i in range(26):
        c = chr(ord('a') + i)
        nume = base_nume + 42 * i
        val = ((6235 + nume) * randomnumber(10, 524, seed)) % 1000000
        encoding_map[val] = c
    return encoding_map

decoding_map = generate_encoding_map()

s = socket.socket()
s.bind(("127.0.0.1", 51035))
s.listen(1)

print("OwOn~...")
while True:
    conn, _ = s.accept()
    data = conn.recv(1024).decode()
    if not data:
        continue

    print("[Base Message]:", data)
    xor_decrypted = xor_decrypt(data, key_for_xor)
    print("[XOR Decrypted]:", xor_decrypted)

    decoded_message = ""
    pairs = xor_decrypted.strip().split()

    for pair in pairs:
        if ":" not in pair:
            decoded_message += "?"
            continue
        val_str, _ = pair.split(":")
        try:
            val = int(val_str)
        except ValueError:
            decoded_message += "?"
            continue

        decoded_message += decoding_map.get(val, "?")

    print("[Decoded Message]:", decoded_message)
