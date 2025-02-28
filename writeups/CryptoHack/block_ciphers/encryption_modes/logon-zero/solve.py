#!/usr/bin/env python

from pwn import *
import json


attack_token = b"\x00" * 28

c = remote("socket.cryptohack.org", 13399)
i = 0
c.recvline()
while True:
    print("Try:", i, end="\r")
    c.sendline(
        json.dumps({"option": "reset_password", "token": attack_token.hex()}).encode()
    )
    c.recvline()

    c.sendline(json.dumps({"option": "authenticate", "password": ""}).encode())
    text = c.recvline()
    if b"admin" in text:
        print("Flag:", json.loads(text)["msg"])
        break
    c.sendline(json.dumps({"option": "reset_connection"}).encode())
    c.recvline()
    i += 1
