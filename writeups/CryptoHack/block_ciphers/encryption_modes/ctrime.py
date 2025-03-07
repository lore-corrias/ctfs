#!/usr/bin/env python

import requests
import string


ENDPOINT = "https://aes.cryptohack.org/ctrime/encrypt/%s"


flag = b"crypto{CRIME_571ll_p4y5}"
base_len = len(
    bytes.fromhex(
        requests.get(ENDPOINT % ((flag + b"}") * 2).hex()).json()["ciphertext"]
    )
)

while flag[-1] != ord("}"):
    for candidate in string.printable:
        encrypted = bytes.fromhex(
            requests.get(ENDPOINT % ((flag + candidate.encode()) * 2).hex()).json()[
                "ciphertext"
            ]
        )
        print("[+] Trying: %s" % (flag + candidate.encode()), len(encrypted), end="\r")
        if len(encrypted) < base_len:
            flag += candidate.encode()
            print("Found:", flag.decode())
            break
    else:
        print("[-] Not found")
        break
