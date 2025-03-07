#!/usr/bin/env python

import requests


ENCRYPT_URL = "https://aes.cryptohack.org/symmetry/encrypt/%s/%s"
FLAG = bytes.fromhex(requests.get("https://aes.cryptohack.org/symmetry/encrypt_flag").json()["ciphertext"])

iv, ciphertext = FLAG[:16], FLAG[16:]
print(bytes.fromhex(requests.get(ENCRYPT_URL % (ciphertext.hex(), iv.hex())).json()["ciphertext"]))
