#!/usr/bin/env python

import requests
from Crypto.Util.strxor import strxor

COOKIE = bytes.fromhex(requests.get("https://aes.cryptohack.org/flipping_cookie/get_cookie/").json()["cookie"])

def check_admin(cookie, iv):
    return requests.get("https://aes.cryptohack.org/flipping_cookie/check_admin/%s/%s" % (cookie.hex(), iv.hex())).json()

blocks = [COOKIE[i:i+16] for i in range(0, len(COOKIE), 16)]
iv = bytearray(blocks[0])

tamper_offset = 6
plaintext_content = b"False"
tamper_content = b"True;"

tamper_iv = blocks[0][tamper_offset:tamper_offset + len(tamper_content)]
iv = iv[:tamper_offset] + strxor(strxor(tamper_iv, plaintext_content), tamper_content) + iv[tamper_offset + len(tamper_content):]

print(check_admin(COOKIE[16:], iv))
