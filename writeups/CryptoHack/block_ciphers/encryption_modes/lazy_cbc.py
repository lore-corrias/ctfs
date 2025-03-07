#!/usr/bin/env python

import requests
from Crypto.Util.strxor import strxor


PLAINTEXT = (b"a" * 16 * 3).hex()
CIPHERTEXT = bytes.fromhex(
    requests.get("https://aes.cryptohack.org/lazy_cbc/encrypt/" + PLAINTEXT).json()[
        "ciphertext"
    ]
)


tampered_ciphertext = (CIPHERTEXT[:16] + b"\x00" * 16 + CIPHERTEXT[:16]).hex()
decrypted_ciphertext = bytes.fromhex(
    requests.get("https://aes.cryptohack.org/lazy_cbc/receive/" + tampered_ciphertext)
    .json()["error"]
    .replace("Invalid plaintext: ", "")
)

key = strxor(decrypted_ciphertext[:16], decrypted_ciphertext[32:48]).hex()
print(
    bytes.fromhex(
        requests.get("https://aes.cryptohack.org/lazy_cbc/get_flag/" + key).json()[
            "plaintext"
        ]
    )
)
