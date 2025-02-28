#!/usr/bin/env python

import requests
from pwn import xor


FLAG = bytes.fromhex(requests.get("https://aes.cryptohack.org/bean_counter/encrypt/").json()["encrypted"])
PNG_HEADER = bytes([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00, 0x00, 0x00, 0x0d, 0x49, 0x48, 0x44, 0x52])


plaintext = b""

enc_k = bytes([PNG_HEADER[i] ^ FLAG[i] for i in range(16)])
plaintext = xor(FLAG, enc_k)

with open("flag.png", "wb") as f:
    f.write(bytes(plaintext))
