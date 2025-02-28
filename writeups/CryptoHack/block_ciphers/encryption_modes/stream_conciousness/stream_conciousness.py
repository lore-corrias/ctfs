#!/usr/bin/env python

import requests
import os


ENCRYPT_ENDPOINT = "https://aes.cryptohack.org/stream_consciousness/encrypt/"


def get_ciphertexts():
    texts = []
    print("[+] Getting 22 unique ciphertexts from website.")
    i = 0
    while len(texts) < 22:
        text = requests.get(ENCRYPT_ENDPOINT).json()["ciphertext"]
        if text not in texts:
            texts.append(text)
        i += 1
    print("[+] Got 22 unique ciphertexts. Took {} requests".format(i))
    return texts


ciphertexts = []
if not os.path.exists("ciphertexts"):
    with open("ciphertexts", "w") as f:
        ciphertexts = get_ciphertexts()
        f.writelines([x + "\n" for x in ciphertexts])
